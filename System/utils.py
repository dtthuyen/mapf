import csv
import time
from typing import List
import numpy as np
import math
import pygame
import os
import datetime

TILE_SIZE = 12

TG1_0 = 0
T1 = 1
TG1_1 = 2
G1 = 3

T2_1 = 4
T2_2 = 4
G2_1 = 5
G2_2 = 5

TG1_2 = 6

T3_1 = 7
T3_2 = 7
T3_3 = 7

G3_1 = 8
G3_2 = 8
G3_3 = 8

DD = 9
XOAY = 10
BD = -1


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


def calculatePointBack(point: list, arrBack: List[list], num_way=3, distance_measure=0):
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


def findWayStage(way: List[dict]):
    """
    Hàm tìm các đoạn thẳng trên đường
    Trả về các điểm đầu và cuối trên các đoạn
    Ví dụ:
    A-----B---------C
                    |
                    |
                    |
                    D-------E
    return [A, B, C, D, E]
    """
    allStage = [0]
    time2goal = 0
    change_his = [False, False]
    for i, point in enumerate(way):
        x_change = False
        y_change = False
        if i != len(way) - 1:
            next_point = way[i + 1]
            if i == 0:
                if abs(next_point["x"] - point["x"]) == 1:
                    change_his[0] = True
                if abs(next_point["y"] - point["y"]) == 1:
                    change_his[1] = True
            if abs(next_point["x"] - point["x"]) == 1:
                x_change = True
            if abs(next_point["y"] - point["y"]) == 1:
                y_change = True
            if [x_change, y_change] != change_his:
                allStage.append(i)
        change_his = [x_change, y_change]
    allStage.append(len(way) - 1)
    return [way[idx] for idx in allStage]


def manhattanDistance(point1: list, point2: list):
    """
    Khoảng cách Manhattan
    """
    return sum(abs(val1 - val2) for val1, val2 in zip(point1, point2))


def matrix(x):
    return x * TILE_SIZE + TILE_SIZE / 2


def read_csv(filename):
    map_data = []
    with open(os.path.join(filename)) as data:
        data = csv.reader(data, delimiter=",")
        for row in data:
            map_data.append(list(row))
    return map_data


arrMap = read_csv("csv_file/map350danhdauvitri.csv")


def blit_text(surface, text, pos, font, color=pygame.Color("black")):
    words = [
        word.split(" ") for word in text.splitlines()
    ]  # 2D array where each row is a list of words.
    space = font.size(" ")[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def draw(arrVarMap, screen, start_time, total_packages=0, AGV_num=0):
    j = 2
    x = 0
    if start_time != 0:
        total_time = time.time() - start_time
    else:
        total_time = 0
    if int(total_time) != 0:
        PPH = int((total_packages * 3600) / int(total_time))
    else:
        PPH = 0
    text = f"""
    ---------------------------------------
    |  So AGV online:   {AGV_num}               | 
    |  Luu luong tong:   {total_packages} |
    |  Thời gian vận hành: {str(datetime.timedelta(seconds=int(total_time)))}|
    |  PPH: {int(PPH / 38)}
    |  So cua nhan hang:   38             |
    |  So cong tra hang:   360            |
    ---------------------------------------
    """
    font = pygame.font.SysFont("Arial", 24)
    blit_text(screen, text, (850, 300), font)
    for point in arrVarMap:
        if x == 0:
            x += 1
            continue
        for i in range(len(point)):
            if point[i] == "":
                pygame.draw.rect(
                    screen,
                    (211, 211, 211),
                    pygame.Rect(
                        (i + 1) * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE
                    ),
                    1,
                )
            if point[i] == "2":
                pygame.draw.rect(
                    screen,
                    (58, 232, 34),
                    pygame.Rect(
                        (i + 1) * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE
                    ),
                )
                pygame.draw.rect(
                    screen,
                    (211, 211, 211),
                    pygame.Rect(
                        (i + 1) * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE
                    ),
                    1,
                )
            if point[i] == "3":
                pygame.draw.rect(
                    screen,
                    (246, 181, 121),
                    pygame.Rect(
                        (i + 1) * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE
                    ),
                )
                pygame.draw.rect(
                    screen,
                    (211, 211, 211),
                    pygame.Rect(
                        (i + 1) * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE
                    ),
                    1,
                )
            if point[i] == "1":
                pygame.draw.rect(
                    screen,
                    (58, 116, 34),
                    pygame.Rect(
                        (i + 1) * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE
                    ),
                )
        j += 1


def VelocityOnWayStage(wayStage: List[dict], t_save=0):
    """
    Hàm để tính vận tốc tức thời tại 1 thời điểm t trên đường đi
    """
    a = 3

    startPoint = [wayStage[0]["x"], wayStage[0]["y"]]
    endpoint = [wayStage[1]["x"], wayStage[1]["y"]]
    print(startPoint, endpoint)
    distance = (
                       abs(startPoint[0] - endpoint[0]) + abs(startPoint[1] - endpoint[1])
               ) / 2
    t = 0
    deltaT = 1 / 24
    temp_V = 0  # Vận tốc tức thời
    temp_position = 0  # Vị trí tức thời
    v_max = 3
    t_dec = None
    V = []

    while True:
        t += 1
        t_save += 1
        if a > 0:
            S = (1 / 2) * a * pow((t * deltaT), 2)
            position = S
            veclocity = a * t * deltaT
            if veclocity >= v_max:
                print("Đạt được tốc độ tối đa")
                veclocity = v_max
                a = 0
                t_dec = t
                temp_position = S
            S0 = (veclocity * veclocity) / (2 * 3)
            if distance - S - S0 <= 0:
                a = -3
                temp_V = veclocity
                temp_position = S
                t_dec = t
            V.append({t_save: position})
        elif a == 0:
            S = v_max * (t - t_dec) * deltaT
            position = temp_position + S
            S0 = (v_max * v_max) / (2 * 3)
            if distance - position - S0 <= 0:
                print("Bắt đầu giảm tốc")
                a = -3
                temp_V = v_max
                temp_position = position
                t_dec = t
            V.append({t_save: position})
        else:
            S = temp_V * (t - t_dec) * deltaT + (1 / 2) * a * pow(
                ((t - t_dec) * deltaT), 2
            )
            veclocity = temp_V + a * (t - t_dec) * deltaT
            position = temp_position + S
            V.append({t_save: position})
            if veclocity <= 0:
                break
    return V, t_save


def calculateTimeOnWay(way: List[dict]):
    allStage = findWayStage(way)
    t = 0
    wayPlan = []
    for i in range(len(allStage) - 1):
        start_point = allStage[i]
        end_point = allStage[i + 1]
        timePlan, t = VelocityOnWayStage([start_point, end_point], t)

        wayPlan.extend(timePlan)

    return wayPlan


def WayToEvent(way: List[dict]):
    allStage = findWayStage(way)
    event = []
    for i in range(len(allStage) - 1):
        startPoint = [allStage[i]["x"], allStage[i]["y"]]
        endpoint = [allStage[i + 1]["x"], allStage[i + 1]["y"]]
        distance = abs(startPoint[0] - endpoint[0]) + abs(startPoint[1] - endpoint[1])
        if distance == 1:
            event.append(BD)
            event.append(TG1_0)
        elif distance == 2:
            event.extend([BD, T1, G1])
            pass
        elif distance == 3:
            event.extend([BD, T1, TG1_1, G1])
            pass
        elif distance == 4:
            event.extend([BD, T2_1, T2_2, G2_1, G2_2])
            pass
        elif distance == 5:
            event.extend([BD, T2_1, T2_2, TG1_2, G2_1, G2_2])
            pass
        elif distance == 6:
            event.extend([BD, T3_1, T3_2, T3_3, G3_1, G3_2, G3_3])
            pass
        elif distance > 6:
            event.extend([BD, T3_1, T3_2, T3_3])
            event.extend([DD] * (distance - 6))
            event.extend([G3_1, G3_2, G3_3])
            pass
    return event


def calculateTimeToDistance(way):
    """
    Hàm tính toán thời gian đi hết đường giao
    """
    time2goal = 0
    change_his = [False, False]
    for i, point in enumerate(way):
        x_change = False
        y_change = False
        if i != len(way) - 1:
            next_point = way[i + 1]
            if i == 0:
                if abs(next_point["x"] - point["x"]) == 1:
                    change_his[0] = True
                if abs(next_point["y"] - point["y"]) == 1:
                    change_his[1] = True
            if abs(next_point["x"] - point["x"]) == 1:
                x_change = True
            if abs(next_point["y"] - point["y"]) == 1:
                y_change = True
            if [x_change, y_change] == change_his:
                time2goal += 4
            elif [x_change, y_change] != change_his:
                time2goal += 16
        change_his = [x_change, y_change]
    return time2goal + 24


def deliveryPoint(x_out: str, y_out: str, arrDelivery: List[list]):
    """
    Hàm để tìm ra các điểm có thể đổ hàng của AGV với rule map.
    """
    arr = []
    x_out, y_out = int(x_out), int(y_out)
    if [x_out + 1, y_out] in arrDelivery:
        arr.append([x_out + 1, y_out])

    if [x_out - 1, y_out] in arrDelivery:
        arr.append([x_out - 1, y_out])

    if [x_out, y_out + 1] in arrDelivery:
        arr.append([x_out, y_out + 1])

    if [x_out, y_out - 1] in arrDelivery:
        arr.append([x_out, y_out - 1])

    return arr


def calculateCost(way: List[dict], crossPoint: list):
    """
    Hàm để tính chi phí đường đi cho AGV
    Dùng chi phí này để lựa chọn đường đi tối ưu cho AGV trong quá trình cấp đường ở server.
    """
    cost = 0
    allStage = findWayStage(way)
    for i in range(len(allStage) - 1):
        startPoint = [allStage[i]["x"], allStage[i]["y"]]
        endpoint = [allStage[i + 1]["x"], allStage[i + 1]["y"]]
        distance = abs(startPoint[0] - endpoint[0]) + abs(startPoint[1] - endpoint[1])
        cost += distance * 0.5
    cost += (len(allStage) - 2) * 3
    for point_dict in way:
        point = [point_dict["x"], point_dict["y"]]
        if point in crossPoint:
            cost += 1
    return int(cost)


def manhattanDistance(point1: list, point2: list):
    return sum(abs(val1 - val2) for val1, val2 in zip(point1, point2))
