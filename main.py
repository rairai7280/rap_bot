#!/bin/envp python
# -*- coding: utf-8 -*-

import MeCab
import requests
import pprint

RHYME_LIMIT=5
VOWEL_DICT={
    "a" : ("ア", "カ", "サ", "タ", "ナ", "ハ", "マ", "ヤ", "ラ", "ワ", "ガ", "ザ", "ダ", "バ", "パ"),
    "i" : ("イ", "キ", "シ", "チ", "ニ", "ヒ", "ミ", "リ", "ギ", "ジ", "ヂ", "ビ", "ピ"),
    "u" : ("ウ", "ク", "ス", "ツ", "ヌ", "フ", "ム", "ユ", "ル", "グ", "ズ", "ヅ", "ブ", "プ"),
    "e" : ("エ", "ケ", "セ", "テ", "ネ", "へ", "メ", "レ", "ゲ", "ザ", "デ", "ベ", "ペ"),
    "o" : ("オ", "コ", "ソ", "ト", "ノ", "ホ", "モ", "ヨ", "ロ", "ヲ", "ゴ", "ゾ", "ド", "ボ", "ポ")
}

def main():
    m = MeCab.Tagger()
    test="僕は元気 色々ありますがなんとかやっています．"
    # 文章毎に処理する
    text_list = test.rstrip().split(" ")
    for i in text_list:
        result_list = list()
        vowels = list()
        res = m.parse(i).split('\n')
        for j in res:
            if not '\t' in j:
                continue
            word, analyse = j.split('\t')
            analyse_list = analyse.split(',')

            result_list.append([word, analyse_list])
        # 文章の終わりの単語を定義
        limit = RHYME_LIMIT
        for k in (reversed(result_list)):
            if limit-len(k[1][8]) < 0:
                break
            else:
                limit -= len(k[1][8])
            vowels.insert(0, extract_vowel(k[1][8]))

        # 母音に合う単語を探す
        vowels = "おおうあ"
        response = requests.get(
            # 'http://rhyme-db.com/search?boin={}'.format(vowels)
            'http://rhyme-db.com/'
        )
        print (response.json())
        # pprint.pprint(response.json())


def extract_vowel(word, kana=True):
    print (word)
    ret = ""
    for c in word:
        vowel = ""
        for k, v in VOWEL_DICT.items():
            if c in v:
                vowel = k
        if vowel == "":
            ret+="-"
        else:
            ret+=vowel
    return ret

if __name__=="__main__":
    main()
