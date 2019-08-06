from datetime import timedelta
import difflib
import os

from flask import Flask, render_template, request, flash, redirect,\
    get_flashed_messages, session, jsonify, url_for,\
    send_from_directory, current_app
from flask_sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
import threading
import queue
import requests

from src import SpiderForm, youdict, hujiang, words_validate, mail


def youdict_spider(threadName, q):
    """
    :param threadName: thread name of threading module
    :param q: Queue object of queue

    Usage::

        get youdict words and store them in the sqlalchemy database
    """
    words = youdict(threadName, q)
    for i in words:
        word = Words(i[0], i[1])
        try:
            db.session.add(word)
            db.session.commit()
        except BaseException:
            pass


def hujiang_spider(threadName, q):
    """
    :param threadName: thread name of threading module
    :param q: Queue object of queue module
    
    Usage::

        get hujiang words and store them in the sqlalchemy database
    """
    words = hujiang(threadName, q)
    for i in words:
        word = Words(i[0], i[1])
        db.session.add(word)
        db.session.commit()


class SpiderThread(threading.Thread):
    """
    :param name: thread name
    :param q: queue object of queue module
    :param website: the words website to scrapy

    :method run:

        run the words scrapy program with threading and queue
    """
    def __init__(self, name, q, website):
        threading.Thread.__init__(self)
        self.name = name
        self.q = q
        self.website = website

    def run(self):
        print("Starting " + self.name)
        while True:
            try:
                if self.website == "youdict":
                    youdict_spider(self.name, self.q)
                elif self.website == "hujiang":
                    hujiang_spider(self.name, self.q)
            except BaseException:
                break
        print("Exiting" + self.name)


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.jinja_env.auto_reload = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(seconds=1)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///words.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_BINDS"] = {
    'wrongwords': 'sqlite:///wrongwords.sqlite3'
}

db = SQLAlchemy(app)


class Words(db.Model):
    """
    :attr|param id: id for words
    :attr|param english: english for words
    :attr|param chinese: chinese explanation for english words
    """
    id = db.Column("words_id", db.Integer, primary_key=True)
    english = db.Column(db.String(30))
    chinese = db.Column(db.String(75))

    def __init__(self, english, chinese):
        self.english = english
        self.chinese = chinese


class WrongWords(db.Model):
    """
    :attr|param id: id for 1wrong words
    :attr|param english: english for wrong words
    :attr|param chinese: chinese explanation for english wrong words
    """
    __bind_key__ = "wrongwords"
    id = db.Column("wrong_words_id", db.Integer, primary_key=True)
    english = db.Column(db.String(30))
    chinese = db.Column(db.String(75))

    def __init__(self, english, chinese):
        self.english = english
        self.chinese = chinese


@app.before_first_request
def before_first_request():
    """
    Usage::

        Before first request for the application, we need to
        initialize some variables and create the databases.
    """
    global choice, failure, is_failure
    global db

    choice = 0
    failure = []
    is_failure = False

    session.permanent = True
    session["recite-progress"] = 0

    db.create_all()
    db.create_all(bind="wrongwords")


@app.route("/")
def main():
    """
    Usage::

        the index page for cishen application
    """
    return render_template("main.html")


@app.route("/see-words", methods=["GET", "POST"])
def see():
    """
    Usage::

        The page for seeing all words in the databases. It can delete
        some words or all words.
    """
    if request.method == "POST":
        delete_all = request.form.get("delete-all")
        print(delete_all)
        if delete_all:
            words = Words.query.all()
            for i in words:
                db.session.delete(i)
            db.session.commit()
            return redirect("/see-words")
        else:
            english = request.form.get("english")
            chinese = request.form.get("chinese")
            u = Words.query.filter_by(english=english, chinese=chinese).first()
            db.session.delete(u)
            db.session.commit()
            return render_template("see-words/see.html",
                                   words=Words.query.all())
    else:
        return render_template("see-words/see.html", words=Words.query.all())


@app.route("/add-new-word", methods=["GET", "POST"])
def new():
    """
    Usage::

        the page for href to use hand or file to add new words. Also accept
        post from hand page.
    """
    if request.method == "GET":
        return render_template("add-new-word/new.html")
    else:
        success, errors = words_validate(request.form.get("words"))
        for data in success:
            word = Words(data[0], data[1])
            db.session.add(word)
        db.session.commit()
        return redirect("see-words")


@app.route("/recite-words/<set>", methods=["GET", "POST"])
def recite(set):
    """
    Usage::

        The page for recite words in the words database. Accept the first
        get and other post for data transmission.
    """
    global choice, failure, is_failure

    if set == "words":
        words_set = Words
    elif set == "wrongwords":
        words_set = WrongWords

    if request.method == "GET":
        recite_progress = session.get("recite-progress")
        if not recite_progress:
            session["recite-progress"] = 0
        choice = session.get("recite-progress")
        words = []

        for i in words_set.query.all():
            words.append(i)
        if words:
            return render_template(
                "recite-words/recite.html", words=words, choice=choice, failure=False)
        else:
            flash("请先添加单词！")
            return redirect("/")
    else:
        words = []
        for i in words_set.query.all():
            words.append(i)
        data = request.form.get("data")
        form_failure = request.form.get("is-failure")
        word = words[choice]

        if is_failure:
            is_failure = True
            word = failure[choice]
        if data:
            if data.upper() == word.english.upper():
                if form_failure:
                    failure.remove(word)
                return render_template(
                    "recite-words/result.html", data=data, word=word, status="答对咯！", failure=is_failure)
            else:
                failure.append(word)
                return render_template(
                    "recite-words/result.html", data=data, word=word, status="答错了！", failure=is_failure)
        else:
            if form_failure:
                is_failure = True
                word = failure[choice]
                failure.remove(word)
                if not failure:
                    choice = 0
                    is_failure = False
                    failure = []
                    flash("复习完成！")
                    return redirect("/")

            choice += 1
            words_count = 20 if not session.get(
                "words_count") else session.get("words_count")
            lst_choice = words_count if not is_failure else len(failure)

            if choice >= len(words) or choice >= lst_choice:
                session["recite-progress"] = choice
                choice = 0
                if not failure:
                    choice = 0
                    is_failure = False
                    failure = []
                    flash("复习完成！")
                    return redirect("/")
                else:
                    for i in failure:
                        if set == Words:
                            wrongwords = WrongWords(i.english, i.chinese)
                        db.session.add(wrongwords)
                    db.session.commit()
                    is_failure = True
                    return render_template(
                        "recite-words/recite.html", words=failure, choice=choice, failure=True)
            return render_template(
                "recite-words/recite.html", words=words, choice=choice)


@app.route("/search-words", methods=["GET", "POST"])
def search():
    """
    Usage::

        The page for search words from words database. Accept get and post of 
        key word for search.
    """
    if request.method == "GET":
        return render_template("search-words/search.html")
    else:
        result = []
        data = request.form.get("data")
        for i in WrongWords.query.all():
            sm = difflib.SequenceMatcher(None, i.english, data)
            if sm.ratio() >= 0.5:
                result.append(i)
        return render_template("search-words/result.html", result=result)


@app.route("/wrong-words", methods=["GET", "POST"])
def wrong_words():
    """
    Usage::

        The page for show wrong words from wrongwords database. Accept get
        and post for deleting.
    """
    if request.method == "POST":
        delete_all = request.form.get("delete-all")
        if delete_all:
            words = WrongWords.query.all()
            for i in words:
                db.session.delete(i)
            db.session.commit()
            return redirect("/wrong-words")
        else:
            english = request.form.get("english")
            chinese = request.form.get("chinese")
            u = WrongWords.query.filter_by(
                english=english, chinese=chinese).first()
            db.session.delete(u)
            db.session.commit()
            return render_template(
                "wrong-words/wrong.html", words=WrongWords.query.all())
    else:
        return render_template("wrong-words/wrong.html",
                               words=WrongWords.query.all())


@app.route("/wrong-words/recite", methods=["GET", "POST"])
def wrong_words_recite():
    """
    Usage::

        The recite page for wrong words. The same as recite words page.
    """
    return redirect("/recite-words/recite/wrongwords")


@app.route("/settings", methods=["GET", "POST"])
def settings():
    """
    Usage::

        The settings page. Settings contains the words count you want to recite
        one time, the scrapy program for two websites.
    """
    youdictform = SpiderForm()
    hujiangform = SpiderForm()
    if request.method == "GET":
        return render_template("/settings/settings.html", words_count=session.get("words_count"),
                               youdictform=youdictform, hujiangform=hujiangform)
    else:
        session["words_count"] = int(request.form.get("words_count"))
        flash("修改设置成功")
        return render_template("/settings/settings.html", words_count=session.get("words_count"),
                               youdictform=youdictform, hujiangform=hujiangform)


@app.route("/spider/<website>", methods=["POST"])
def youdict_spider_post(website):
    """
    :param website: the website name to scrapy

    Usage::

        The page for scrapy website operation. Accept post
        with website name.
    """
    # print(website)
    youdictform = SpiderForm()
    hujiangform = SpiderForm()
    link_list = []
    if website == "youdict":
        page_number_begin = youdictform.page_number_begin.data
        page_number_all = youdictform.page_number_all.data

        finish = page_number_begin + page_number_all
    elif website == "hujiang":
        page_number_begin = hujiangform.page_number_begin.data
        page_number_all = hujiangform.page_number_all.data

        finish = page_number_begin + page_number_all

    if finish > 2239 or finish < 0 or finish % 1 != 0:
        flash("非法的页数")
        return redirect("/settings")

    for i in range(page_number_begin, finish):
        if website == "youdict":
            url = f"https://www.youdict.com/ciku/id_0_0_0_0_{i}.html"
        elif website == "hujiang":
            url = f"https://www.hujiang.com/ciku/zuixinyingyudanci_{i}"
        link_list.append(url)
    # print(link_list)

    threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5"]
    workQueue = queue.Queue(2500)
    threads = []

    for tName in threadList:
        thread = SpiderThread(tName, workQueue, website)
        thread.start()
        threads.append(thread)

    for url in link_list:
        workQueue.put(url)

    for t in threads:
        t.join()

    return redirect("/see-words")


@app.route("/word-books")
def word_books():
    """
    Usage::

        The word books page. The word books is used for
        download the prepared words. It is faster than scrapy.
    """
    return render_template("word-books/books.html")


@app.route("/word-books/download/<name>", methods=["POST"])
def word_books_download(name):
    """
    :param name: the name of the word book

    Usage::

        The word books download page for only post method. Word books can be
        download here and added to the words databases.
    """
    file = "./static/word-books/" + name + ".txt"
    f = open(file, "r", encoding="utf-8").read()
    url = url_for("new", _external=True)
    requests.post(url, data={"words": f})
    return redirect("/see-words")


@app.route("/add-new-word/hand")
def hand():
    """

    Usage::

        The page for add new word by hand. Have a post for add new word
        index page to transmit word data.
    """
    return render_template("add-new-word/hand.html")


@app.route("/add-new-word/file", methods=["GET", "POST"])
def file():
    if request.method == "POST":
        try:
            f = request.files['file']
            filename = secure_filename(f.filename)
            f.save(filename)
            with open(filename, "r", encoding="utf-8") as f:
                success, errors = words_validate(f.read())
            os.remove(filename)
            for data in success:
                word = Words(data[0], data[1], data[2])
                db.session.add(word)
            db.session.commit()
            os.remove(filename)
            return render_template("see-words/see.html",
                                   words=Words.query.all())

        except UnicodeDecodeError:
            return render_template(
                "add-new-word/failure1.html", filename=filename)
        except Exception:
            return render_template(
                "add-new-word/failure2.html", filename=filename)
    else:
        return render_template("add-new-word/file.html")


@app.errorhandler(404)
def four_zero_four(exception):
    """
    Usage::

        The 404 page for this flask application.
    """
    return render_template("404.html", exception=exception)


@app.errorhandler(500)
def five_zero_zero(exception):
    """
    Usage::

        The 500 page for this flask application.
    """
    mail(exception)
    return render_template("500.html")


@app.route('/favicon.ico')
def favicon():
    """
    Usage::

        The favicon for every page.
    """
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(port=33507)
