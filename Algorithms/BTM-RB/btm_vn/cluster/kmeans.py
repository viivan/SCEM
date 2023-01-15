"""
包括我们sDPC算法和普通KMeans算法
"""
import numpy as np
from sklearn.cluster import KMeans
import random
import math
import matplotlib.pyplot as plt


def kMeansByFeature(k, matrix):
    data = np.array(matrix)
    estimator = KMeans(n_clusters=k)
    estimator = estimator.fit(data)
    return estimator


def cal_distance(vec1, vec2):
    # 直接计算欧式距离的平方
    d_sum = sum([math.pow(vec1[i] - vec2[i], 2) for i in range(len(vec1))])
    return d_sum


def cal_distance_threshold(matrix):
    # 计算截断距离dc
    c = []
    d = []
    for vec in matrix:
        # 和除了自己以外的元素距离
        di = [cal_distance(vec, i) for i in matrix if i != vec]
        di.sort()
        c.append(di)
    for ci in c:
        ai = []
        for i in range(len(ci) - 1):
            ai.append(ci[i + 1] - ci[i])
        # 将差值对应的距离组较小的一个加入
        ai_max = max(ai)
        index = ai.index(ai_max)
        d.append(ci[index])
    return min(d)


def cal_density(threshold, matrix):
    # 计算dpc中元素局部密度,threshold为截断距离
    des = []
    for i in matrix:
        d = [cal_distance(i, v) for v in matrix if v != i]
        count = 0
        for x in d:
            if x < threshold:
                count += 1
        des.append(count)
    return des


def cal_element_distance(density, matrix):
    # 计算dpc中元素间距离,density为局部密度
    e_d = []
    d_max = max(density)
    for i in range(len(density)):
        if d_max == density[i]:  # 密度最大
            d = [cal_distance(matrix[i], j) for j in matrix]
            e_d.append(max(d))
        else:
            d = [cal_distance(matrix[i], matrix[j]) for j in range(len(matrix)) if density[j] > density[i]]
            e_d.append(min(d))
    return e_d


def init_random_center(k, matrix):
    # 返回随机中心点向量
    center_result = set()
    while len(center_result) < k:
        center_result.add(int(str(random.random() * len(matrix)).split('.')[0]))  # 整数部分
    result = []
    for i in center_result:
        result.append(matrix[i])
    return result


def init_dpc_center(k, matrix):
    # 利用dpc算法实现
    # 计算截断距离，局部密度，元素距离
    threshold = cal_distance_threshold(matrix)
    density = cal_density(threshold, matrix)
    ele_distance = cal_element_distance(density, matrix)
    r = [density[i] * ele_distance[i] for i in range(len(density))]
    # 选择r中值最大的k个元素作为聚类中心
    c_index = []
    used = [0] * len(r)
    while len(c_index) < k:
        m_r = [r[i] for i in range(len(r)) if used[i] == 0]
        r_m = max(m_r)
        index = -1
        for i in range(len(r)):
            if used[i] == 0:
                if r[i] == r_m:
                    index = i
                    break
        c_index.append(index)
        used[index] = 1
    # 将对应的序号转化为元素矩阵
    center = [matrix[i] for i in c_index]
    return center


def clustering(clusters, center, matrix):
    # 初始化簇字典
    for i in range(len(center)):
        clusters[i] = []

    # 找到就近的点归类
    for i in range(len(matrix)):
        distances = [0] * len(center)
        for j in range(len(center)):
            distances[j] = cal_distance(center[j], matrix[i])
        d_min = min(distances)
        d_index = distances.index(d_min)
        clusters[d_index].append(matrix[i])


def cal_center(clusters, matrix):
    # 计算新的中心点
    center = []
    for i in clusters:
        cluster = clusters[i]
        blank_vec = np.array([0] * len(matrix[0]), 'float32')
        for c in cluster:
            blank_vec += np.array(c, 'float32')
        if len(cluster) != 0:
            blank_vec /= len(cluster)
        center.append(list(blank_vec))
    return center


def change_result_type(clusters, matrix):
    # 改写聚类结果形式
    cluster_result = [0] * len(matrix)
    for i in clusters:
        cluster = clusters[i]
        for c in cluster:
            index = matrix.index(c)
            cluster_result[index] = i
    return cluster_result


def simple_kMeans(k, matrix, iterate):
    # 使用随机的初始聚类中心
    center = init_random_center(k, matrix)
    """
    for j in matrix:
        plt.plot(j[0], j[1], "bo-")
    for c in center:
        plt.plot(c[0], c[1], "ro-")
    plt.show()
    """
    print("center:{}".format(center))
    clusters = {}  # 用字典来存储，对应key为序号

    # 开始聚类
    for i in range(iterate):
        print("cluster round:{}".format(i))
        clustering(clusters, center, matrix)
        center = cal_center(clusters, matrix)
        print("center:{}".format(center))
        """
        for j in matrix:
            plt.plot(j[0], j[1], "bo-")
        for c in center:
            plt.plot(c[0], c[1], "ro-")
        plt.show()
        """
    # 改写聚类结果形式，输出
    cluster_result = change_result_type(clusters, matrix)
    return cluster_result


def dpc_kMeans(k, matrix, iterate):
    # sDPC算法
    center = init_dpc_center(k, matrix)
    clusters = {}  # 用字典来存储，对应key为序号
    print("center:{}".format(center))
    # 开始聚类
    for i in range(iterate):
        print("cluster round:{}".format(i))
        clustering(clusters, center, matrix)
        center = cal_center(clusters, matrix)
        # print("center:{}".format(center))

    # 改写聚类结果形式，输出
    cluster_result = change_result_type(clusters, matrix)
    return cluster_result


def top_cluster(matrix):
    # 简单将分布中最高的那个分量作为类结果
    cluster_result = []
    for m in matrix:
        m_max = max(m)
        max_index = list(m).index(m_max)
        cluster_result.append(max_index)
    return cluster_result


if __name__ == "__main__":
    c_k = 3
    c_iterator = 100
    p_data = [[0, 1], [0, 0], [1, 0], [3, 3], [3, 5], [4, 3]]

    c_result = simple_kMeans(c_k, p_data, c_iterator)
    print(c_result)

    # d_c_result = dpc_kMeans(c_k, p_data, c_iterator)
    # print(d_c_result)
