#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
# @Time    : 20-6-20 下午4:56

# @Author  : zhufa

# @Software: PyCharm
"""
"""
利用RectangularContourFinder类进行查找矩形区域
"""
import cv2
import RectangularContourFinder
import numpy as np

image = cv2.imread("testImg/2.jpg")
cv2.imshow('img', image)
# 实例化类
rectangularContourFinder = RectangularContourFinder.RectangularContourFinder(image)
# 查找符合条件的矩形轮廓
result = rectangularContourFinder.getRectContour(option=RectangularContourFinder.OUTSIDE_ONLY)
# 对上一步返回的轮廓根据条件进行排序
sortedresult1 = rectangularContourFinder.sortByMinAreaRect_centerPiont(result, image)

sortedresult2 = rectangularContourFinder.sortByBoundingRect_leftTopPiont(result, image)
g = np.array(sortedresult2)[:, 3]
for h in range(len(g)):
    cv2.imshow(str(h), g[h])
l = 1
for s in sortedresult2:
    ssss = str(l) + '-(' + str(s[0][0]) + ',' + str(s[0][1]) + ')'
    ss = s[2]
    cv2.drawContours(image, s[0], -1, (0, 0, 255), 1)
    cv2.putText(image, str(l) + '-(' + str(int(s[2][0])) + ',' + str(int(s[2][1])) + ')', (int(s[1][0]), int(s[1][1])),
                cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, (255, 255, 0), 1)
    l = l + 1
cv2.imshow('result', image)
cv2.waitKey()
