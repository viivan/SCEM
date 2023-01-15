import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from gensim import corpora as corp

"""
文档预处理
分句，分词，提取词语主干
"""

# 获取英语的停止词
stop = stopwords.words("english")
# 获取wordNet词形还原帮助类
lemma = WordNetLemmatizer()


def isSymbol(word):
    return bool(re.match(r'[^\w]', word))


def hasNumber(word):
    return bool(re.search(r'\d', word))


def check(word):
    if isSymbol(word):
        return False
    if hasNumber(word):
        return False
    return True


def divide(doc):
    # 对每个文档进行分句，分词，归一化处理
    # doc为单文档字符串
    sentences = nltk.sent_tokenize(doc)
    words = []
    for sentence in sentences:
        word_list = nltk.word_tokenize(sentence)
        for word in word_list:
            word = word.lower()
            if check(word) and not (word in stop):
                # 归一形态
                temp = lemma.lemmatize(word)
                # 获取词根
                lem = wordnet.morphy(word)
                if lem is None:
                    words.append(word)
                else:
                    words.append(lem)
    return words


def get_doc_after_divide(doc, num=5):
    # 获取完整处理后的语料信息，返回为dictionary
    # doc为为文档字典，未分词, num为对应的低频词频率
    dic = {}
    word_list = []
    whole_dic = []
    # 先进行第一步分词
    for k in doc:
        document = doc[k]
        words = divide(document)
        word_list.append(words)
        whole_dic += words

    # 计算词频，建立低词频list
    low_word = cal_low_fre_word(whole_dic, num)

    # 去除
    t = 0
    for k in doc:
        words = word_list[t]
        document = ""
        for w in words:
            if w not in low_word:
                document += w
                document += " "
        # 如果全为低频词，保留两个词以免出错
        if document == "":
            document += words[0] + " " + words[1] + " "
        document = document[0:len(document)-1]
        dic[k] = document
        t += 1

    return dic


def cal_low_fre_word(word_list, num=5):
    # 计算语料中低频词并去除,默认为出现5次以下
    # word_list为语料主干化分词后的结果
    low_word = []
    word_set = set(word_list)
    for word in word_set:
        if word_list.count(word) < num:
            low_word.append(word)
    return low_word
