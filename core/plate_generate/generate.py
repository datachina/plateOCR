# -*-coding:utf-8 -*-
"""
Description: 
Author: John Holl
Github: https://github.com/hzylyh
Date: 2022/4/23 13:28
LastEditors: John Holl
LastEditTime: 2022/4/23 13:28
"""
import os
from PIL import ImageFont
from core.plate_generate.common import *


index = {"京": 0, "沪": 1, "津": 2, "渝": 3, "冀": 4, "晋": 5, "蒙": 6, "辽": 7, "吉": 8, "黑": 9,
         "苏": 10, "浙": 11, "皖": 12, "闽": 13, "赣": 14, "鲁": 15, "豫": 16, "鄂": 17, "湘": 18, "粤": 19,
         "桂": 20, "琼": 21, "川": 22, "贵": 23, "云": 24, "藏": 25, "陕": 26, "甘": 27, "青": 28, "宁": 29,
         "新": 30, "0": 31, "1": 32, "2": 33, "3": 34, "4": 35, "5": 36, "6": 37, "7": 38, "8": 39,
         "9": 40, "A": 41, "B": 42, "C": 43, "D": 44, "E": 45, "F": 46, "G": 47, "H": 48, "J": 49,
         "K": 50, "L": 51, "M": 52, "N": 53, "P": 54, "Q": 55, "R": 56, "S": 57, "T": 58, "U": 59,
         "V": 60, "W": 61, "X": 62, "Y": 63, "Z": 64}

chars = ["京", "沪", "津", "渝", "冀", "晋", "蒙", "辽", "吉", "黑",
         "苏", "浙", "皖", "闽", "赣", "鲁", "豫", "鄂", "湘", "粤",
         "桂", "琼", "川", "贵", "云", "藏", "陕", "甘", "青", "宁",
         "新",
         "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
         "A", "B", "C", "D", "E", "F", "G", "H", "J", "K",
         "L", "M", "N", "P", "Q", "R", "S", "T", "U", "V",
         "W", "X", "Y", "Z"]


font_ch_file = r"./data/font/platech.ttf"
font_letter_file = r"./data/font/platechar.ttf"
plate_dim_file = r"./data/image/smu2.jpg"
plate_interference_bg = r"./data/NoPlates"


class GenPlate:
    def __init__(self, template=None, plate_type='blue'):
        self.plate_type = plate_type
        self.fontC = ImageFont.truetype(font_ch_file, 43, 0)
        self.fontE = ImageFont.truetype(font_letter_file, 60, 0)
        self.img = np.array(Image.new("RGB", (226, 70), (255, 255, 255)))
        #         self.img = np.array(Image.new("RGB", (226, 70),(0, 0, 0)))
        self.bg = cv.resize(cv.imread(template), (226, 70))
        # template.bmp:车牌背景图
        self.smu = cv.imread(plate_dim_file)
        # smu2.jpg:模糊图像
        self.noplates_path = []
        for parent, parent_folder, filenames in os.walk(plate_interference_bg):
            for filename in filenames:
                path = parent + "/" + filename
                self.noplates_path.append(path)

    def draw(self, val):
        offset = 2
        self.img[0:70, offset + 8:offset + 8 + 23] = GenCh(self.fontC, val[0])
        self.img[0:70, offset + 8 + 23 + 6:offset + 8 + 23 + 6 + 23] = GenCh1(self.fontE, val[1])
        for i in range(5):
            base = offset + 8 + 23 + 6 + 23 + 17 + i * 23 + i * 6
            self.img[0:70, base:base + 23] = GenCh1(self.fontE, val[i + 2])
        return self.img

    def generate(self, text):
        fg = self.draw(text)  # 得到白底黑字
        # cv.imwrite('01.jpg', fg)
        if self.plate_type == 'blue':
            fg = cv.bitwise_not(fg)  # 得到黑底白字
            # cv.imwrite('02.jpg', fg)
            com = cv.bitwise_or(fg, self.bg)  # 字放到车牌背景中
            # cv.imwrite('03.jpg', com)
        else:
            com = cv.bitwise_and(fg, self.bg)  # 字放到车牌背景中
            # cv.imwrite('03.jpg', com)
        com = rot(com, r(30) - 10, com.shape, 30)  # 矩形-->平行四边形
        # cv.imwrite('04.jpg', com)
        com = rotRandrom(com, 5, (com.shape[1], com.shape[0]))  # 旋转
        # cv.imwrite('05.jpg', com)
        com = tfactor(com)  # 调灰度
        # cv.imwrite('06.jpg', com)
        com = random_envirment(com, self.noplates_path)  # 放入背景中
        # cv.imwrite('07.jpg', com)
        com = AddGauss(com, 1 + r(4))  # 加高斯平滑
        # cv.imwrite('08.jpg', com)
        com = addNoise(com)  # 加噪声
        # cv.imwrite('09.jpg', com)
        return com

    def gen_plate_string(self, iter, perSize):
        """
        生成车牌string，存为图片
        生成车牌list，存为label
        """
        plateStr = ""
        plateList = []
        i = iter // perSize
        for cpos in range(7):
            if cpos == 0:
                plateStr += chars[i]
                plateList.append(plateStr)
            elif cpos == 1:
                plateStr += chars[41 + r(24)]
                plateList.append(plateStr)
            else:
                plateStr += chars[31 + r(34)]
                plateList.append(plateStr)
        plate = [plateList[0]]
        b = [plateList[i][-1] for i in range(len(plateList))]
        plate.extend(b[1:7])
        return plateStr, plate

    def gen_batch(self, per_size, output_path, size):
        """
        将生成的车牌图片写入文件夹，对应的label写入label.txt
        :param per_size: 每个省多少条数据
        :param output_path: 输出图像的保存路径
        :param size: 输出图像的尺寸
        :return: None
        """
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        for i in range(per_size*31-1):
            plate_str, plate = self.gen_plate_string(i, per_size)
            img = self.generate(plate_str)
            img = cv.resize(img, size)
            cv.imwrite(output_path + "/" + plate_str + ".jpg", img)
