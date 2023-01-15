import math
from nltk.corpus import wordnet as wn
import sys
from six import iteritems 


def computeSim(w1, w2):
    L = 1000000
    minSyn = None
    s1 = wn.synsets(w1)
    s2 = wn.synsets(w2)
    for si in s1 :
        hash1 = si._shortest_hypernym_paths(False)
        node1 = list(hash1.keys())
        for sj in s2:
            node2 = []
            hash2 = {}
            start = 0
            end = 1
            node2.append(sj)
            hash2.update({sj : 0})
            while start < end :
                s3 = node2[start].hypernyms()
                for sk in s3:
                    if sk not in hash2 :
                        node2.append(sk)
                        hash2.update({sk: 1})
                        end += 1
                    if sk in hash1 :
                        v = hash1.get(sk) + hash2.get(sk)
                        if v < L:
                            L = v
                            minSyn = sk
                start += 1
    # 追踪到root节点的路径 WordNet中的root节点就是entity
    if not minSyn is None:
        D = minSyn.shortest_path_distance(wn.synsets('entity')[0])
    else:
        D = -1
    print(minSyn)
    return [L,D]



result = computeSim(sys.argv[1], sys.argv[2])
print(result[0], result[1])