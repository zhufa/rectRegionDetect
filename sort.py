#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
# @Time    : 20-6-19 下午5:46

# @Author  : zhufa

# @Software: PyCharm
"""

"""
坐标排序：从上到下，从左到右排序
"""

a = [[4, 5], [2, 4], [3, 4], [1, 1], [2, 5]]
a1 = sorted(a, key=lambda s: s[1] * 1000 + s[0])
a2 = sorted(a, key=lambda s: (s[1], s[0]))
print a[0]
a3 = sorted(a2, key=lambda s: s[3:5])
print a1
print a2
print a3


# 网上排序方法：冒泡排序
def zuobiaopaixu(a):
    b = []
    l = len(a)
    for i in range(l):
        j = i
        for j in range(l):
            if (a[i][0] < a[j][0]):
                a[i], a[j] = a[j], a[i]
            if (a[i][1] < a[j][1]):
                a[i], a[j] = a[j], a[i]
    for k in range(len(a)):
        b.append(a[k])
    return b


# 我的排序方法
def mySort(a):
    b = []
    b.append(a[0])
    for i in range(1, len(a)):
        for j in range(len(b)):
            if a[i][1] < b[j][1]:
                b.insert(j, a[i])
            elif a[i][1] > b[j][1]:
                b.append(a[i])
            # elif a[i][1] == b[j][1]:


b = zuobiaopaixu(a)
# print b
