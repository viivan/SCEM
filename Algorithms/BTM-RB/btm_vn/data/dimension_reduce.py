"""
数据降维处理
使用t-sne库，将数据处理为二维数据
输出后续使用plot处理转化为散点图
"""
from sklearn.manifold import TSNE
import numpy as np


def dimension_down(data):
    r = np.array(data)
    tsne = TSNE(n_components=2)
    x = tsne.fit_transform(r)
    x_min = np.min(x, 0)  # 获取整个矩阵中最左下的坐标点
    x_max = np.max(x, 0)  # 获取整个矩阵中最右上的坐标点
    x = (x - x_min) / (x_max - x_min)  # 向量归一化
    return x.tolist()


if __name__ == "__main__":
    d = [[1, 2, 3], [1, 4, 6], [3, 6, 5]]
    result = dimension_down(d)
    print(result)