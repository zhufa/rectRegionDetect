#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
# @Time    : 20-6-17 下午5:25

# @Author  : zhufa

# @Software: PyCharm
"""

import cv2
import numpy as np

image = cv2.imread("testImg/1.jpg")
# image = cv2.resize(image, (0, 0), fx= 0.5, fy= 0.5, interpolation= cv2.INTER_NEAREST)
cv2.imshow('img', image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('gray', gray)
# thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,3,5)
# thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,3,5)
# _,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
'''
gaussblur = cv2.GaussianBlur(gray,(3,3),0)
gradX = cv2.Sobel(gaussblur,cv2.CV_32F,1,0,ksize=-1)
gradY = cv2.Sobel(gaussblur,cv2.CV_32F,0,1,ksize=-1)
sobleX = cv2.convertScaleAbs(gradX)
sobleY = cv2.convertScaleAbs(gradY)
add = cv2.addWeighted(sobleX,1,sobleY,1,1)
cv2.imshow('add', add)
_,thresh = cv2.threshold(add,127,255,cv2.THRESH_BINARY_INV)
'''
cv2.imshow('thresh', thresh)

dilate = cv2.dilate(thresh, (10, 100), iterations=5)
cv2.imshow('dilate', dilate)
close1 = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, (10, 10), iterations=3)
cv2.imshow('close1', close1)
open1 = cv2.morphologyEx(close1, cv2.MORPH_OPEN, (1, 1), iterations=3)
cv2.imshow('open1', open1)
img, cnts, hiera = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
# cnts = sorted(cnts,key=cv2.contourArea,reverse=True)

j = 1
lastCenter = None
result = []
for i in range(len(cnts)):

    d = (cnts[i][0][0][0], cnts[i][0][0][1])
    a = cv2.contourArea(cnts[i])
    center, size, angle = cv2.minAreaRect(cnts[i])
    [leftTopPiont_x, leftTopPiont_y, width, height] = cv2.boundingRect(cnts[i])
    B = cv2.boundingRect(cnts[i])
    p1 = (int(center[0] - size[0] / 2), int(center[1] - size[1] / 2))
    center = (int(center[0]), int(center[1]))
    if hiera[0][i][3] == -1:
        continue

    # cv2.circle(image,center,5,(0,0,255),1)
    # cv2.rectangle(image,p1,p2,(0,0,255),1)
    a1 = size[0] * size[1]
    s = str(i) + ',' + str(a) + ',' + '%.2f' % a1
    if a > 800 and a / a1 > 0.9:
        cv2.drawContours(image, cnts, i, (0, 0, 255), 1)
        # cv2.putText(image,str(j) + '-('+ str(B[2])+','+str(B[3]) + ')',(B[0],B[1]),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,0.5,(255,255,0),1)
        j = j + 1
        result.append([[B[0], B[1]], [B[2], B[3]]])

ss = sorted(result, key=lambda s: s[0][1] * 10000 + s[0][0])
l = 0
for s in ss:
    ssss = str(l) + '-(' + str(s[0][0]) + ',' + str(s[0][1]) + ')'
    s1 = s[1]
    cv2.putText(image, str(l) + '-(' + str(s[1][0]) + ',' + str(s[1][1]) + ')', (s[0][0], s[0][1]),
                cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, (255, 255, 0), 1)
    l = l + 1
cv2.imshow('result', image)
cv2.waitKey()
