from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from model import word2vecAdapter as w2v

"""
利用sklearn库进行tf_idf矩阵计算
返回词典list 
返回文档对应每个词list
"""


def sort_method(element):
    return element[2]


def cal_tf_idf(doc={}):
    # 传入参数为以name为key的预处理后的文档内容
    corpus = []
    for n in doc:
        document = doc[n]
        corpus.append(document)

    vector = CountVectorizer()  # 获取词汇解释器
    transformer = TfidfTransformer()  # tf-idf计算
    tf_idf = transformer.fit_transform(vector.fit_transform(corpus))
    word_dic = vector.get_feature_names()  # 获取词汇矩阵
    weight = tf_idf.toarray()  # 每个文档对于每个词的tf_idf值

    return word_dic, weight


def keyword_by_tf_idf(doc={}, num=5):
    # num为留下的keyword数
    # 传入参数为以name为key的预处理后的文档内容
    corpus = []
    name = []
    for n in doc:
        document = doc[n]
        corpus.append(document)
        name.append(n)

    vector = CountVectorizer()  # 获取词汇解释器
    transformer = TfidfTransformer()  # tf-idf计算

    frequency = vector.fit_transform(corpus)
    tf_idf = transformer.fit_transform(frequency)

    word_dic = vector.get_feature_names()  # 获取词汇矩阵
    weight = tf_idf.toarray()  # 每个文档对于每个词的tf_idf值
    frequency_array = frequency.toarray()  # 词频矩阵

    new_doc = {}
    for i in range(len(weight)):
        # 将id，频率fre，weight，zip起来sort完了获取前num个词
        w = weight[i]
        fre = frequency_array[i]
        id_fre_w = list(zip(range(len(weight[i])), fre, w))
        id_fre_w.sort(key=sort_method, reverse=True)  # 倒序排序
        # print(id_fre_w)
        t = 0
        doc_string = ""
        for j in range(len(id_fre_w)):
            if t < num:
                # 频率不为0
                if id_fre_w[j][1] != 0:
                    for q in range(id_fre_w[j][1]):
                        doc_string += word_dic[id_fre_w[j][0]]+" "
                    t += 1
            else:
                break
        new_doc[name[i]] = doc_string

    return new_doc


def expend_word(model, doc, num=5, sim_num=3):
    # model为w2v模型，doc为文档，num为被扩容的单词数, sim_num为扩容数
    corpus = []
    name = []
    for n in doc:
        document = doc[n]
        corpus.append(document)
        name.append(n)

    print("计算tf_idf")
    vector = CountVectorizer()  # 获取词汇解释器
    transformer = TfidfTransformer()  # tf-idf计算

    frequency = vector.fit_transform(corpus)
    tf_idf = transformer.fit_transform(frequency)

    word_dic = vector.get_feature_names()  # 获取词汇矩阵
    weight = tf_idf.toarray()  # 每个文档对于每个词的tf_idf值
    frequency_array = frequency.toarray()  # 词频矩阵

    print("开始拓展")
    for i in range(len(weight)):
        # 将id，频率fre，weight，zip起来sort
        w = weight[i]
        fre = frequency_array[i]
        id_fre_w = list(zip(range(len(weight[i])), fre, w))
        id_fre_w.sort(key=sort_method, reverse=True)  # 倒序排序
        t = 0
        for j in range(len(id_fre_w)):
            if t < num:
                if id_fre_w[j][1] != 0:
                    ex_list = w2v.word_expand(model, word_dic[id_fre_w[j][0]], sim_num)
                    for e in ex_list:
                        doc[name[i]] += (" "+e)
                    t += 1
            else:
                break
    return doc


if __name__ == "__main__":
    doc = {"1": "this is the first document",
           "2": "this is the second second document",
           "3": "and the third one",
           "4": "is this the first document",
           "5": "no of course"}
    # new_d = keyword_by_tf_idf(doc)
    model = w2v.load_model_binary(r"")
    doc = expend_word(model, doc, 5, 3)
    print(doc)
