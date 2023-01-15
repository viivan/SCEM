# biterm 是包含两个词的词组合
class Biterm:
    """
    包含两个词的对应词典id 从小到大 word1,word2
    包含对应的topic
    包含该biterm的使用频率(全局)
    """
 
    def __init__(self, index, word1, word2):
        # word1与word2为对应的词id，小的在前
        if word1 > word2:
            self.word1 = word2
            self.word2 = word1
        else:
            self.word1 = word1
            self.word2 = word2
        self.topic = 0
        self.freq = 0
        self.index = index

    def __cmp__(self, bit):
        # 比较函数，方便去重
        if bit.word1 == self.word1 and bit.word2 == self.word2:
            return True
        else:
            return False

    def __str__(self):
        return "word 1:{} word2:{}".format(self.word1, self.word2)

