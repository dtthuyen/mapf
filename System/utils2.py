import csv
import math
from typing import List

import numpy as np


def mPoint(xX, yY, map_size=[68, 68]):
    # 68 hang (y), 68 cot(x)
    temp = 0
    temp = (yY - 1) * map_size[0] + xX
    return temp


def load_map_to_list(map_csv):
    csv_file = open(map_csv)
    csv_reader = csv.reader(csv_file, delimiter=",")
    map_rows = []
    for row in csv_reader:
        map_rows.extend(row)
    print(len(map_rows))
    return map_rows


def pMatrixInt(sttP, map_size=[68, 68]):
    print("index: ", sttP)
    xX = sttP % map_size[0]
    yY = sttP // map_size[0] + 1
    if xX == 0:
        xX = map_size[0]
        yY = int(sttP / map_size[0])
    temp = [xX, yY]
    return temp


def convertWay(arrPoint):
    arrOut = []
    for p in arrPoint:
        temp = pMatrixInt(p)
        arrOut.append(temp)
    return arrOut


def makeDeliveryPointForOutPort(outport):
    x, y = pMatrixInt(outport)
    return [mPoint(x + 1, y), mPoint(x - 1, y), mPoint(x, y - 1), mPoint(x, y + 1)]


def loadPointPort(csv_path):
    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        arrOut = []
        i = 0
        for row in csv_reader:
            # print (row[0],',',row[1])
            temCo = [int(row[0]), int(row[1])]
            arrOut.append(temCo)
            i += 1
        print("Đọc {} dòng từ file {}".format(i, csv_path))
    # arrOut = pd.unique(arrOut).tolist()
    return arrOut


def xytoStr(xy):
    temp = '"' + str(xy[0]) + "," + str(xy[1]) + '"'
    return temp


def convertWay2String(way: list):
    wayStr = ""
    for point in way:
        wayStr += str(point[0]) + "," + str(point[1]) + "\n"
    return wayStr


def convertPoint2String(point: list):
    return str(point[0]) + "," + str(point[1])


def convertWay1dToString(way: list):
    wayStr = ""
    for point in way:
        wayStr += str(point) + "\n"
    return wayStr


def caculatePointBack(point: list, arrBack: List[list], num_way=3, distance_measure=0):
    distance = []
    for index, backPoint in enumerate(arrBack):
        if distance_measure != 0:
            dis = math.sqrt(
                math.pow((point[0] - backPoint[0]), 2)
                + math.pow((point[1] - backPoint[1]), 2)
            )
        else:
            dis = manhattanDistance(point, backPoint)
        distance.append(dis)
    distance = np.array(distance)
    index_sort = np.argsort(distance)
    returnPoint = []
    for i in range(num_way):
        returnPoint.append(arrBack[index_sort[i]])
    return returnPoint


def manhattanDistance(point1: list, point2: list):
    return sum(abs(val1 - val2) for val1, val2 in zip(point1, point2))


def load_map_to_list(map_csv):
    csv_file = open(map_csv)
    csv_reader = csv.reader(csv_file, delimiter=",")
    map_rows = []
    for row in csv_reader:
        map_rows.extend(row)
    print(len(map_rows))
    return map_rows
