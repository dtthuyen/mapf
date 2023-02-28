import csv
from collections import defaultdict

from tqdm import tqdm

from utils import loadPointPort, makeDeliveryPointForOutPort, mPoint, pMatrixInt

fileway = open("baseLine3.txt", "r")
listWay = fileway.readlines()
print(len(listWay))
allWay = []
for way in listWay:
    way = eval(way)
    # print(way, type(way))
    allWay.append(way)
del fileway
del listWay


arrOutport = loadPointPort("csv/arrOutput.csv")
arrmPointOut = [mPoint(x[0], x[1]) for x in arrOutport]
soOutportHasWay = 0

listBaseLineFinal = defaultdict(list)
for i in tqdm(range(len(arrmPointOut))):
    outport = arrmPointOut[i]
    deliveryPoint = makeDeliveryPointForOutPort(outport)
    has = False
    for i, way in enumerate(allWay):
        if len({*deliveryPoint} & {*way["hasOut"]}):
            listBaseLineFinal[outport].append(way)
            has = True
    if has:
        soOutportHasWay += 1
        continue
    if not has:
        print("out port ko co base line: ", pMatrixInt(outport))
    # print("==============================")

print(soOutportHasWay == len(arrOutport))
print(len(list(listBaseLineFinal.keys())))
print("chien")


finalBaseLineDict = dict()
for ouport in listBaseLineFinal.keys():
    # print(outport)
    listWay = listBaseLineFinal[ouport]
    cost = 9999
    finalWay = way
    for way in listWay:
        if way["weights"] < cost:
            finalWay = way
            cost = way["weights"]
    finalBaseLineDict[ouport] = way
