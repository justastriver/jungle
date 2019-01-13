# coding: utf-8
import jieba.posseg as pseg
 
words = pseg.cut("15亿光年神秘太空信号王源粉丝")
for word, flag in words:
    print("%s %s" % (word, flag))
