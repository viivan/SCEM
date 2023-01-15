from gensim.models import word2vec
from gensim.models import KeyedVectors

"""
使用word2vec获取词语的特征信息 
"""

size = 10


def build_model(text_path=r"", save_path=r""):
    print("载入语料数据")
    sentences = word2vec.Text8Corpus(text_path)
    print("进行模型训练")
    model = word2vec.Word2Vec(sentences, size=size)  # size为词向量维度，窗口默认为5
    print("训练完成")
    model.wv.save_word2vec_format(save_path, binary=True)  # 二进制存储
    print("训练模型保存完成，地址:{}".format(save_path))
    return model


def load_model_binary(save_path=r"E:\学校\快乐推荐\word2vec\saveVec"):
    print("加载模型文件{}".format(save_path))
    model = KeyedVectors.load_word2vec_format(save_path, binary=True)
    print("加载完毕")
    return model


def wordlist_to_vec(model, word_list):
    vec_list = []
    for word in word_list:
        # 词汇表中存在则进行处理,不存在直接使用0矩阵
        if word in model.index2word:
            vec_list.append(model[word])
        else:
            vec_list.append([0] * len(model["hello"]))
        # print("word:{}, vec:{}".format(word, vec_list[len(vec_list)-1]))
    return vec_list


def word_expand(model, word, num=3):
    # 进行给定词近义词的扩充，num指定扩充数量
    if word in model.index2word:
        expand_list = model.most_similar(word, topn=num)
        expand_word_list = []
        for w in expand_list:
            expand_word_list.append(w[0])
        return expand_word_list
    else:
        return []

