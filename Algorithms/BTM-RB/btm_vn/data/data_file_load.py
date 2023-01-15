"""
数据文件读取方法
"""

import os

# 获取路径信息
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("btm_vn\\") + len("btm_vn\\")]


def loadWordSimMatrix(sim_filename):
    # 读取词汇相似度矩阵文件，list形式
    sim_save_path = os.path.abspath(rootPath + "resource\\" + sim_filename)
    sim_matrix = []
    try:
        sf = open(sim_save_path, "r+")
        lines = sf.readlines()
        for line in lines:
            line = line.strip()
            simple_line_list = line.split(" ")
            simple_line_list = [float(x) for x in simple_line_list]
            sim_matrix.append(simple_line_list)
    except IOError:
        print("读取相似度文件失败")
    return sim_matrix


def loadWordIndexMatrix(word_index_filename):
    # 读取文档词汇序号矩阵，D行
    # int matrix
    word_index_save_path = os.path.abspath(rootPath + "resource\\" + word_index_filename)
    word_index_matrix = []
    try:
        wf = open(word_index_save_path, "r+")
        lines = wf.readlines()
        for line in lines:
            line = line.strip()
            int_line = line.split(",")
            int_line = [int(x) for x in int_line]
            word_index_matrix.append(int_line)
    except IOError:
        print("读取文档词汇序号文件失败")
    return word_index_matrix


def loadVocabularyList(voc_filename):
    # 读取词汇表
    voc_save_path = os.path.abspath(rootPath + "resource\\" + voc_filename)
    voc_list = []
    try:
        vf = open(voc_save_path, "r+")
        lines = vf.readlines()
        for line in lines:
            line = line.strip()
            voc_list.append(line)
    except IOError:
        print("读取词汇序表文件失败")
    return voc_list
