# -*-coding:utf-8 -*-
"""
Description: 
Author: John Holl
Github: https://github.com/hzylyh
Date: 2022/4/23 13:26
LastEditors: John Holl
LastEditTime: 2022/4/23 13:26
"""
import cv2 as cv
import numpy as np
from math import *

from PIL import Image
from PIL import ImageDraw


def AddSmudginess(img, Smu):
    """
    模糊处理
    :param img: 输入图像
    :param Smu: 模糊图像
    :return: 添加模糊后的图像
    """
    rows = r(Smu.shape[0] - 50)
    cols = r(Smu.shape[1] - 50)
    adder = Smu[rows:rows + 50, cols:cols + 50]
    adder = cv.resize(adder, (50, 50))
    img = cv.resize(img, (50, 50))
    img = cv.bitwise_not(img)
    img = cv.bitwise_and(adder, img)
    img = cv.bitwise_not(img)
    return img


def rot(img, angel, shape, max_angel):
    """
    添加透视畸变
    """
    size_o = [shape[1], shape[0]]
    size = (shape[1] + int(shape[0] * cos((float(max_angel) / 180) * 3.14)), shape[0])
    interval = abs(int(sin((float(angel) / 180) * 3.14) * shape[0]))
    pts1 = np.float32([[0, 0], [0, size_o[1]], [size_o[0], 0], [size_o[0], size_o[1]]])
    if angel > 0:
        pts2 = np.float32([[interval, 0], [0, size[1]], [size[0], 0], [size[0] - interval, size_o[1]]])
    else:
        pts2 = np.float32([[0, 0], [interval, size[1]], [size[0] - interval, 0], [size[0], size_o[1]]])
    M = cv.getPerspectiveTransform(pts1, pts2)
    dst = cv.warpPerspective(img, M, size)
    return dst


def rotRandrom(img, factor, size):
    """
    添加放射畸变
    :param img: 输入图像
    :param factor: 畸变的参数
    :param size: 图片目标尺寸
    :return: 放射畸变后的图像
    """
    shape = size
    pts1 = np.float32([[0, 0], [0, shape[0]], [shape[1], 0], [shape[1], shape[0]]])
    pts2 = np.float32([[r(factor), r(factor)], [r(factor), shape[0] - r(factor)], [shape[1] - r(factor), r(factor)],
                       [shape[1] - r(factor), shape[0] - r(factor)]])
    M = cv.getPerspectiveTransform(pts1, pts2)
    dst = cv.warpPerspective(img, M, size)
    return dst


def tfactor(img):
    """
    添加饱和度光照的噪声
    """
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    hsv[:, :, 0] = hsv[:, :, 0] * (0.8 + np.random.random() * 0.2)
    hsv[:, :, 1] = hsv[:, :, 1] * (0.3 + np.random.random() * 0.7)
    hsv[:, :, 2] = hsv[:, :, 2] * (0.2 + np.random.random() * 0.8)
    img = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
    return img


def random_envirment(img, noplate_bg):
    """
    添加自然环境的噪声, noplate_bg为不含车牌的背景图
    """
    bg_index = r(len(noplate_bg))
    env = cv.imread(noplate_bg[bg_index])
    env = cv.resize(env, (img.shape[1], img.shape[0]))
    bak = (img == 0)
    bak = bak.astype(np.uint8) * 255
    inv = cv.bitwise_and(bak, env)
    img = cv.bitwise_or(inv, img)
    return img


def GenCh(f, val):
    """
    生成中文字符
    """
    img = Image.new("RGB", (45, 70), (255, 255, 255))  # 白色
    #     img = Image.new("RGB", (45, 70), (0, 0, 0))  #黑色
    draw = ImageDraw.Draw(img)
    #     draw.text((0, 3), val, (0, 0, 0), font=f)
    draw.text((0, 3), val, (0, 0, 0), font=f)
    img = img.resize((23, 70))
    A = np.array(img)
    return A


def GenCh1(f, val):
    """
    生成英文字符
    """
    img = Image.new("RGB", (23, 70), (255, 255, 255))  # 白色
    #     img =Image.new("RGB", (23, 70), (0, 0, 0))#黑色
    draw = ImageDraw.Draw(img)
    draw.text((0, 2), val, (0, 0, 0), font=f)  # val.decode('utf-8')
    A = np.array(img)
    return A


def AddGauss(img, level):
    """
    添加高斯模糊
    """
    return cv.blur(img, (level * 2 + 1, level * 2 + 1))


def r(val):
    return int(np.random.random() * val)


def AddNoiseSingleChannel(single):
    """
    添加高斯噪声
    """
    diff = 255 - single.max()
    noise = np.random.normal(0, 1 + r(6), single.shape)
    noise = (noise - noise.min()) / (noise.max() - noise.min())
    noise *= diff
    # noise= noise.astype(np.uint8)
    dst = single + noise
    return dst


def addNoise(img):  # sdev = 0.5,avg=10
    img[:, :, 0] = AddNoiseSingleChannel(img[:, :, 0])
    img[:, :, 1] = AddNoiseSingleChannel(img[:, :, 1])
    img[:, :, 2] = AddNoiseSingleChannel(img[:, :, 2])
    return img



