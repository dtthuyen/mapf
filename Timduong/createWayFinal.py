import csv
from collections import defaultdict
from tqdm import tqdm
import __redis as re
from graphUtils import Edge, Graph
# from sql2 import importTempWay, importWayBack
from utils import (
    convertPoint2String,
    convertWay,
    convertWay1dToString,
    convertWay2String,
    load_map_to_list,
    loadPointPort,
    makeDeliveryPointForOutPort,
    mPoint,
    pMatrixInt,
    caculatePointBack,
)


def checkEgde(point, direction):
    if direction == "r":
        checkPoint = mPoint(point[0] + 1, point[1])
        return map_rows[checkPoint - 1], pMatrixInt(checkPoint)
    elif direction == "u":
        checkPoint = mPoint(point[0], point[1] - 1)
        return map_rows[checkPoint - 1], pMatrixInt(checkPoint)
    elif direction == "l":
        checkPoint = mPoint(point[0] - 1, point[1])
        return map_rows[checkPoint - 1], pMatrixInt(checkPoint)
    elif direction == "d":
        checkPoint = mPoint(point[0], point[1] + 1)
        return map_rows[checkPoint - 1], pMatrixInt(checkPoint)


def convertCrossPoint2FinalWay(crossWay: list, map_rows: list):
    path = []
    path.append(crossWay[0])
    for i in range(len(crossWay)):
        start_point = crossWay[i]
        if i == len(crossWay) - 1:
            break
        end_point = crossWay[i + 1]
        # print("xet {} va {}".format(start_point, end_point))
        startLocation = mPoint(start_point[0], start_point[1])

        start_direct = map_rows[startLocation - 1]
        # print(start_direct.split(","))
        for direct in start_direct.split(","):
            pathTemp = []
            result = direct
            crossGoal = start_point
            while len(result) == 1:
                result, crossGoal = checkEgde(crossGoal, result)
                pathTemp.append(crossGoal)
                # print("duong di ", crossGoal)
                if crossGoal in arrCorner:
                    break
            if pathTemp[-1] == end_point:
                path.extend(pathTemp)
                continue
            # print("===============")
    return path


print("=================== Load tất cả các file cần thiết ===========================")
day = "040122"
csv_folder = f"csv{day}/"
map_path = csv_folder + f"map350_{day}_X.csv"
arrIP_path = csv_folder + "arrInput.csv"
arrOP_path = csv_folder + "arrOutput.csv"
arrBack_path = csv_folder + "arrBack.csv"
arrDelivery_path = csv_folder + "arrDelivery.csv"
IDelivery_path_file = csv_folder + "IP2DeliveryWay.csv"

arrCross_path = csv_folder + "arrPointTotal.csv"
arrCorner_path = csv_folder + "arrCorner.csv"

map_rows = load_map_to_list(map_path)

arrIP = loadPointPort(arrIP_path)
arrCross = loadPointPort(arrCross_path)
arrOutport = loadPointPort(arrOP_path)
arrCorner = loadPointPort(arrCorner_path)
arrBack = loadPointPort(arrBack_path)
arrDelivery = loadPointPort(arrDelivery_path)
allDeliveryPoint = []

for i in tqdm(range(len(arrOutport))):
    outport = arrOutport[i]
    outport = mPoint(outport[0], outport[1])
    allDeliveryPoint.extend(makeDeliveryPointForOutPort(outport))

allEdges = []

# them duong co so dua tren diem Corner
for crossPoint in arrCross:  # tim tu corner den corner, cross den corner
    crossLocation = mPoint(xX=crossPoint[0], yY=crossPoint[1])
    direction = map_rows[crossLocation - 1]
    index = 1
    startPoint = None

    for direct in direction.split(","):
        result = direct
        crossGoal = crossPoint
        weight = 0
        hasOut = False
        diemdohang = []

        while len(result) == 1:
            try:
                result, crossGoal = checkEgde(crossGoal, result)
            except:
                print(f"Xet diem crossPoint {crossGoal} {result}")
            weight += 1
            if mPoint(crossGoal[0], crossGoal[1]) in allDeliveryPoint:
                hasOut = True
                diemdohang.append(mPoint(crossGoal[0], crossGoal[1]))
            if crossGoal in arrCorner:
                break
        if crossGoal != crossPoint:
            allEdges.append(
                Edge(
                    source=crossLocation,
                    dest=mPoint(crossGoal[0], crossGoal[1]),
                    hasOut=hasOut,
                    weight=weight,
                    diemdohang=diemdohang,
                )
            )

print(len(allEdges))

for inPort in arrIP:
    if inPort in arrCross:
        continue
    inPortLocation = mPoint(xX=inPort[0], yY=inPort[1])
    direct = map_rows[inPortLocation - 1]
    result = direct
    crossGoal = inPort
    weight = 0
    hasOut = False
    diemdohang = []
    while len(result) == 1:
        result, crossGoal = checkEgde(crossGoal, result)
        weight += 1
        if mPoint(crossGoal[0], crossGoal[1]) in allDeliveryPoint:
            hasOut = True
            diemdohang.append(crossGoal)
        if crossGoal in arrCorner:
            break
    if crossGoal != inPort:
        allEdges.append(
            Edge(
                source=inPortLocation,
                dest=mPoint(crossGoal[0], crossGoal[1]),
                hasOut=hasOut,
                weight=weight,
                diemdohang=diemdohang,
            )
        )

print(len(allEdges))
graphMap = Graph(len(allEdges))
graphMap.addEdge(edges=allEdges)

graphMap.findBaseLine()
graphMap.create_Simple_egde()


print(
    "=================== Tìm đường cơ sở cho tất cả các out port ==========================="
)
fileway = open("baseLine.txt", "r")
listWay = fileway.readlines()
print(len(listWay))
allWay = []
for way in listWay:
    way = eval(way)
    allWay.append(way)
del fileway
del listWay

print("Số lượng đường cơ sở được lưu lại: ", len(allWay))


arrOutport = loadPointPort(arrOP_path)
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
    print("==============================")

print('soOutportHasWay',soOutportHasWay == len(arrOutport))
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


print(
    "=================== Tìm đường trả hàng từ inport đến outport dựa trển các điểm delivery ==========================="
)
IOway = open(IDelivery_path_file)
IOway = csv.reader(IOway, delimiter=",")
list_IOway = []
for row in IOway:
    list_IOway.append(row)
print(len(list_IOway))

for i in tqdm(range(len(list_IOway))):
    IO_point = list_IOway[i]
    # print("tim duong {}".format(IO_point))

    inPort = IO_point[0]
    outPort = IO_point[1]
    x_in, y_in = inPort.split(",")
    x_out, y_out = outPort.split(",")
    inPort = mPoint(int(x_in), int(y_in))
    outport = mPoint(int(x_out), int(y_out))

    goal = outport

    PathIO = graphMap.a_star_algorithm(inPort, goal)

    if PathIO is None:
        print("khong tim thay duong {}".format(IO_point))
        assert "Khong tim thay duong"
    else:
        path1d = convertWay1dToString(PathIO)
        PathIO = convertWay(PathIO)
        start = convertPoint2String(PathIO[0])
        end = convertPoint2String(PathIO[-1])
        goal = convertPoint2String(pMatrixInt(outport))
        pathDetail = convertCrossPoint2FinalWay(PathIO, map_rows)

        # PathIO = convertWay2String(PathIO)
        pathDetail = convertWay2String(pathDetail)
        # importTempWay(name="", path=PathIO, path1d=path1d, pdetail=pathDetail, cost="", start=start, end=end,
        #             goal=goal)
        PathIO = convertCrossPoint2FinalWay(PathIO, map_rows)
        re.set_coordinate_to_redis(PathIO, IO_point[0], IO_point[1])
#
# print(
#     "=================== Tìm đường về từ outport về đường default ==========================="
# )

# create way back to default path
# for outport in finalBaseLineDict.keys():
#     baseLine = finalBaseLineDict[outport]
#     endPoint = baseLine["end"]
#     x_end, y_end = pMatrixInt(endPoint)
#     backPoints = caculatePointBack(
#         point=[x_end, y_end], arrBack=arrBack, num_way=5
#     )  # using manhattan distance to find the point back.
#     for backPoint in backPoints:
#         src = mPoint(x_end, y_end)
#         goal = mPoint(backPoint[0], backPoint[1])
#         PathIO = graphMap.a_star_algorithm(src, goal)
#         if PathIO is None:
#             print("khong tim thay duong {}".format((x_end, y_end, backPoint)))
#             print(graphMap.graph[mPoint(1, 2)][0].dest)
#             assert "Khong tim thay duong"
#         else:
#             path1d = convertWay1dToString(PathIO)
#             PathIO = convertWay(PathIO)
#             PathIO = convertCrossPoint2FinalWay(PathIO, map_rows)
#             start_str = str(x_end) + "," + str(y_end)
#             end_str = str(backPoint[0]) + "," + str(backPoint[1])
#
#             # pathDetail = convertCrossPoint2FinalWay(PathIO, map_rows)
#             # PathIO = convertWay2String(PathIO)
#             # pathDetail = convertWay2String(pathDetail)
#             # importWayBack(name="", path=PathIO, pdetail=pathDetail, cost="", start=start_str, end=end_str,
#             #             goal=end_str)
#             re.set_coordinate_wayBack_to_redis(PathIO, start_str, end_str)
#         # print("==================================")

# Tìm đường về từ các điểm delivery
for outport in arrDelivery:
    x_end, y_end = outport
    backPoints = []
    # backPoints = caculatePointBack(
    #     point=[x_end, y_end], arrBack=arrBack, num_way=5
    # )  # using manhattan distance to find the point back.
    for point in arrBack:
        if x_end == point[0]:
            backPoints = [point]
            break
    for backPoint in backPoints:
        src = mPoint(x_end, y_end)
        goal = mPoint(backPoint[0], backPoint[1])
        PathIO = graphMap.a_star_algorithm(src, goal)
        if PathIO is None:
            print("khong tim thay duong {}".format((x_end, y_end, backPoint)))
            print(graphMap.graph[mPoint(1, 2)][0].dest)
            assert "Khong tim thay duong"
        else:
            path1d = convertWay1dToString(PathIO)
            PathIO = convertWay(PathIO)
            PathIO = convertCrossPoint2FinalWay(PathIO, map_rows)
            start_str = str(x_end) + "," + str(y_end)
            end_str = str(backPoint[0]) + "," + str(backPoint[1])
            re.set_coordinate_wayBack_to_redis(PathIO, start_str, end_str)
#         # print("==================================")