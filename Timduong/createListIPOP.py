import csv
import os

import numpy as np


def xytoStr(xy):
    temp = '"' + str(xy[0]) + "," + str(xy[1]) + '"'
    # print(temp)
    return temp


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
        print("So phan tu: ", i)
    return arrOut

day = "040122"
csv_folder = f"csv{day}/"

arrIP = loadPointPort(csv_folder + "arrInput.csv")
arrOP = loadPointPort(csv_folder + "arrOutput.csv")
arrDelivery = loadPointPort(csv_folder + "arrDelivery.csv")

def createList(arrIP: list, arrOP: list):
    listPoint = []
    for pointI in arrIP:
        for pointO in arrOP:
            if pointI != pointO:
                temp = [xytoStr(pointI), xytoStr(pointO)]
                listPoint.append(temp)
            else:
                print(pointI, pointO)
    return listPoint


listOut = createList(arrIP, arrDelivery)
# print(listOut)
np.savetxt(csv_folder + "IP2DeliveryWay.csv", listOut, fmt="%s", delimiter=",")

# arrIP = loadPointPort("arrInput.csv")
# arrOP = loadPointPort("arrPoint.csv")
# listIP_cross = createList(arrIP, arrOP)
# np.savetxt("IP2Point.csv", listIP_cross, fmt="%s", delimiter=",")
