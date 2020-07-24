#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import cv2

"""
查找图像中的矩形轮廓
"""

"""
# @Time    : 20-6-20 下午2:59

# @Author  : zhufa

# @Software: PyCharm
"""

FINDALL = 0
OUTSIDE_ONLY = 1
INSIDE_ONLY = 2


class RectangularContourFinder:

    def __init__(self, image):
        self.image = image

    def getRectContour(self, minArea=800.0, maxArea=float("inf"), threshold=0.9, THRESH_BINARY_INV=True,
                       option=FINDALL):
        """
        返回满足参数限定条件的轮廓
        :param minArea: 轮廓的最小面积阈值
        :param maxArea: 轮廓的最大面积阈值
        :param threshold: 矩形可信度阈值，越大表示轮廓必须越接近矩形
        :param THRESH_BINARY_INV: 是否需要反色查找轮廓，因为通常轮廓查找是基于黑色背景白色物体的轮廓
        :param option: 筛选内轮廓还是外轮廓
        :return: 轮廓Contours
        """

        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        if THRESH_BINARY_INV:
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        else:
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)

        img, cnts, hiera = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

        result = []
        for i in range(len(cnts)):

            contourArea = cv2.contourArea(cnts[i])
            center, size, angle = cv2.minAreaRect(cnts[i])
            minRectArea = size[0] * size[1]

            if option == OUTSIDE_ONLY:
                if hiera[0][i][3] != -1:
                    continue
            elif option == INSIDE_ONLY:
                if hiera[0][i][3] == -1:
                    continue
            elif option != FINDALL:
                return None

            if minArea < contourArea < maxArea and contourArea / minRectArea > threshold:
                result.append(cnts[i])
        return result

    # 需要注意的是，有些虽然眼看着在同一水平线的contours，其实调试会发现他们会有细微的高度差，造成排序的不一样
    def sortByMinAreaRect_centerPiont(self, contours, image, reverse=False):
        """
        对传入的contours进行排序，按contours的MinAreaRect的center坐标，从上到下，从左到右排序
        :param contours: contours列表
        :param image: contours的原图
        :param reverse: 是否反向排序
        :return: 排序好的contours，并且带有contours的MinAreaRect返回信息
        """
        imageWidth = image.shape[1]
        result = []
        for c in contours:
            center, size, angle = cv2.minAreaRect(c)
            result.append([c, center, size, angle])
        sortedresult = sorted(result, key=lambda s: s[1][1] * imageWidth + s[1][0], reverse=reverse)
        return sortedresult

    # 需要注意的是，有些虽然眼看着在同一水平线的contours，其实调试会发现他们会有细微的高度差，造成排序的不一样
    def sortByBoundingRect_leftTopPiont(self, contours, image, reverse=False):
        """
        对传入的contours进行排序，按contours的BoundingRect的左上角坐标，从上到下，从左到右排序
        :param contours: contours列表
        :param image: contours的原图
        :param reverse: 是否反向排序
        :return: 排序好的contours，并且带有contours的BoundingRect返回信息，以及根据boundingRect从原图截取出的区域
        """
        imageWidth = image.shape[1]
        result = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            result.append([c, [x, y], [w, h], image[y:y + h, x:x + w]])
        sortedresult = sorted(result, key=lambda s: s[1][1] * imageWidth + s[1][0], reverse=reverse)
        return sortedresult
