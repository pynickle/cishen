with open("youdict.txt", "r", encoding="utf-8") as f:
    res = f.readlines()

words = []
english_lst = []

for word in res:
    if not word.strip():
        continue
    k = word.split(' ', 1)
    english = k[0]
    chinese = k[1]
    if english in english_lst:
        continue
    dct = (english, chinese)
    words.append(dct)
    english_lst.append(english)

words.sort(key = lambda i: i[0])
with open("test.txt", "a", encoding="utf-8") as f:
    for word in words:
        f.write(word[0] + " " + word[1])
