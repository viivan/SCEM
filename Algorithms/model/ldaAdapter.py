from gensim import corpora, models

'''
使用gensim库中lda实现
传入参数为对应的文档dictionary 
'''

# 存对应的文档名，便于之后确认
name = []
doc = {}


def ldaAdapter(num=3):
    # 参数为主题数量
    # name存放文档名称list
    # doc为对应文档名称-文档词字符串对
    wordlist = []
    for k in doc:
        # document为list，包含预处理后的词
        document = doc[k]
        name.append(k)
        words = str(document).split(" ")
        wordlist.append(words)
    # print(wordlist)
    # 词典创建
    dictionary = corpora.Dictionary(wordlist)
    # print(dictionary.token2id)
    # 词频矩阵创建
    corpus = [dictionary.doc2bow(words) for words in wordlist]
    # 调用lda模型,训练
    lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num)

    """
    for topic in lda.print_topics(num_words=5):
        # 输出主题——词汇矩阵
        print(topic)

    for index, values in enumerate(lda.inference(corpus)[0]):
        # 输出文档——主题矩阵
        print("doc name:{}".format(name[index]))
        for topic, value in enumerate(values):
            print("topic {}: {}".format(topic, value))
    """

    return lda, corpus

