import re
import time
import random
import pprint
import os

import requests
import threading
import queue

class SpiderThread(threading.Thread):
    def __init__(self, name, q, website):
        threading.Thread.__init__(self)
        self.name = name
        self.q = q
        self.website = website
    # run
    def run(self):
        print("Starting " + self.name)
        while True:
            try:
                if self.website == "youdict":
                    result = youdict(self.name, self.q)
                elif self.website == "hujiang":
                    result = hujiang(self.name, self.q)
                # print(result)
            except:
                break
        print("Exiting" + self.name)


headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3858.0 Safari/537.36"}

def youdict(threadName, q):
    res = []
    index = 0
    url = q.get(timeout = 3)
    print(q.qsize())
    index += 1
    r = requests.get(url, headers = headers, timeout = 20)
    html = str(r.content, encoding="utf-8").replace("\n", "").replace("    ", "")
    html = re.sub(r'<span class="yd-kw-suffix">(.*?)</span>', "", html)
    words = re.findall('<div class="caption"><h3 style="margin-top: 10px;"><a style="color:#333;" target="_blank" href="/w/.*?">(.*?)</a>[ ]?</h3><p>(.*?)</p></div>', html)

    for word in words:
        res.append(word)
    if index%5 == 0:
        time.sleep(3 + random.random())
    else:
        time.sleep(1 + random.random())
    generate_txt(res, "youdict.txt")

def hujiang(threadName, q):
    res = []
    index = 0
    url = q.get(timeout = 3)
    print(q.qsize())
    
    index += 1
    r = requests.get(url, headers=headers, timeout=10)
    html = str(r.content, encoding="utf-8").replace("\n", "").replace("    ", "")
    html = re.sub(r'<span class="yd-kw-suffix">(.*?)</span>', "", html)
    words = re.findall('<li class="clearfix"><a href="/ciku/(.*?)/" target="_blank">.*?</a><span>(.*?)</span></li>', html)
    for word in words:
        res.append(word)
        
    if index%5 == 0:
        time.sleep(3 + random.random())
    else:
        time.sleep(1 + random.random())
    generate_txt(res, "hujiang.txt")

def generate_txt(res, filename):
    with open(filename, "a", encoding="utf-8") as f:
        for i in res:
            print(i)
            english = i[0]
            chinese = i[1].replace("\n", " ")
            f.write(english + " " + chinese + "\n")

def scrapy(website):
    link_list = []
    for i in range(100, 292):
        if website == "youdict":
            url = f"https://www.youdict.com/ciku/id_1_0_0_0_{i}.html"
        elif website == "hujiang":
            url = f"https://www.hujiang.com/ciku/zuixinyingyudanci_{i}"
        link_list.append(url)

    threadList = []
    for i in range(1, 11):
        threadList.append("Thread-" + str(i))
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

def main():

    scrapy("youdict")

if __name__ == "__main__":
    main()
