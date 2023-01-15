"""
计算多项聚类准确度的结果
"""
import judge.clustereffect as ce

 
def printResult(k, result, former):
    # result为聚类结果，如【0，0，0，1，1，2，2】
    # former为原始类别，形式与result相同

    pur = ce.purityClusterResult(k, result, former)
    ri = ce.R1ClusterResult(k, result, former)
    en = ce.entropyClusterResult(k, result, former)
    pre = ce.precision_cluster(k, result, former)
    recall = ce.recall_cluster(k, result, former)
    f1 = ce.f1measure_cbq(pre, recall)  # 此处直接求pre与recall的平均

    print("纯度:{}, RI:{}, 熵：{}, 准确率：{}，召回率：{}, F1_measure:{}".format(pur, ri, en, pre, recall, f1))
    result_list = [pur, ri, en, pre, recall, f1]
    return result_list
