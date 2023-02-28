import csv
import json
import time
from collections import defaultdict
from os import path

from tqdm import tqdm

from utils import (
    convertWay,
    loadPointPort,
    makeDeliveryPointForOutPort,
    mPoint,
    pMatrixInt,
)

outfile = open("baseLine.txt", "w")


class Way:
    def __init__(self, start, end, path, weights, hasOut):
        self.start = start
        self.end = end
        self.weights = weights
        self.hasOut = hasOut
        self.path = path

    def get_path(self):
        return self.path

    def get_len(self):
        return len(self.path)


class Edge:
    def __init__(self, source, dest, hasOut, weight, diemdohang=[]):
        self.source = source  # diem di
        self.dest = dest  # diem den
        self.weight = weight  # trong so
        self.hasOut = hasOut
        self.diemdohang = diemdohang


class Graph:
    def __init__(self, verties):
        # No. of vertices
        self.V = verties

        # default dictionary to store graph
        self.graph = defaultdict(list)
        self.adjac_lis = defaultdict(list)
        self.h = dict()

    def get_neighbors(self, v):
        return self.adjac_lis[v]

    def get_len(self):
        return len(self.graph)

    def addEdge(self, edges):
        for edge in edges:
            self.graph[edge.source].append(edge)

    def findAvailablePath(self, arrInput):
        visited = [False] * (68 * 68)
        paths = []
        iter = 0
        while iter < 10:
            print("================{}==================".format(iter + 2))
            for vertice1 in self.graph.keys():
                for vertice2 in self.graph.keys():
                    if vertice1 == vertice2:
                        continue
                    edges_check = [edge.dest for edge in self.graph[vertice1]]
                    if vertice2 not in edges_check:
                        continue
                    for edge in self.graph[vertice1]:
                        # xet truong hop 2 dinh co canh va 1 dinh la input
                        if vertice2 == edge.dest and iter == 0:
                            tempWay = Way(
                                vertice1,
                                vertice2,
                                [vertice1, vertice2],
                                edge.weight,
                                hasOut=[],
                            )
                            paths.append(tempWay)
                            outfile.write(str(tempWay.__dict__) + "\n")

                            if vertice1 % 68 == 0:
                                print("them duong: ", convertWay([vertice1, vertice2]))

                            visited[vertice1] = True
                        elif vertice2 == edge.dest and vertice1 not in arrInput:

                            for path_ in paths:
                                newpath = path_.get_path().copy()
                                if len(newpath) != iter + 1:
                                    continue
                                newpath.append(vertice2)
                                if vertice1 == path_.end:
                                    newpath = path_.get_path().copy()
                                    newpath.append(vertice2)
                                    hasOut = path_.hasOut
                                    if len(edge.diemdohang) > 0:
                                        hasOut.extend(edge.diemdohang)
                                    tempWay = Way(
                                        start=path_.start,
                                        end=vertice2,
                                        path=newpath,
                                        weights=path_.weights + edge.weight,
                                        hasOut=hasOut,
                                    )
                                    paths.append(tempWay)
                                    outfile.write(str(tempWay.__dict__) + "\n")
                                    if path_.start % 68 == 0:
                                        print("them duong: ", convertWay(newpath))
            iter += 1
        return paths

    def findAvailablePath_2(self, listIO):
        for idx in tqdm(range(len(listIO))):
            IO = listIO[idx]
            inPort = IO[0]
            outPort = IO[1]
            deliveryPoint = makeDeliveryPointForOutPort(outPort)
            print(
                "tim duong tu {} den {}".format(pMatrixInt(inPort), pMatrixInt(outPort))
            )
            iter = 0
            paths = []
            while iter < 100:
                path4check = [path_.get_path() for path_ in paths]
                print("=============================")
                for vertice1 in self.graph.keys():
                    for vertice2 in self.graph.keys():
                        if vertice1 == vertice2:
                            continue
                        edges_check = [edge.dest for edge in self.graph[vertice1]]
                        if vertice2 not in edges_check:
                            continue
                        # xet canh cua dinh 1
                        for edge in self.graph[vertice1]:
                            # xet truong hop 2 dinh co canh va 1 dinh la input
                            if (
                                vertice2 == edge.dest
                                and vertice1 == inPort
                                and iter == 0
                            ):
                                paths.append(
                                    Way(
                                        vertice1,
                                        vertice2,
                                        [vertice1, vertice2],
                                        edge.weight,
                                        hasOut=[],
                                    )
                                )
                                print(
                                    "them duong: ",
                                    convertWay([vertice1, vertice2]),
                                    iter,
                                )
                            # continue
                            # xet truong hop 2 dinh co canh nhung 1 dinh khong la input
                            elif vertice2 == edge.dest and vertice1 != inPort:

                                for path_ in paths:
                                    newpath = path_.get_path().copy()
                                    newpath.append(vertice2)
                                    if newpath in path4check:
                                        continue
                                    # kiem tra neu dinh 1 da la diem cuoi cung cua 1 way
                                    # thi append tao ra duong moi
                                    if vertice1 == path_.end:
                                        print(
                                            convertWay(path_.path),
                                            "vertice 1: {}, vertice2 {}".format(
                                                pMatrixInt(vertice1),
                                                pMatrixInt(vertice2),
                                            ),
                                        )
                                        # print(abc)
                                        newpath = path_.get_path().copy()
                                        newpath.append(vertice2)
                                        hasOut = path_.hasOut
                                        if len(edge.diemdohang) > 0:
                                            hasOut.extend(edge.diemdohang)
                                        if path_.get_len() > 6 and not edge.hasOut:
                                            continue
                                        way_temp = Way(
                                            start=path_.start,
                                            end=vertice2,
                                            path=newpath,
                                            weights=path_.weights + edge.weight,
                                            hasOut=hasOut,
                                        )
                                        if len({*deliveryPoint} & {*way_temp.hasOut}):
                                            print(
                                                "duong di tu inPort {} den OutPort {} la: {}".format(
                                                    pMatrixInt(inPort),
                                                    pMatrixInt(outPort),
                                                    convertWay(way_temp.path),
                                                )
                                            )
                                            break
                                        paths.append(
                                            Way(
                                                start=path_.start,
                                                end=vertice2,
                                                path=newpath,
                                                weights=path_.weights + edge.weight,
                                                hasOut=hasOut,
                                            )
                                        )
                iter += 1
        return paths

    def findBaseLine(self):
        baseLine = []
        for vertice1 in self.graph.keys():
            # for vertice2 in listPoint:
            for vertice2 in self.graph.keys():
                if vertice1 == vertice2:
                    continue
                edges_check = [edge.dest for edge in self.graph[vertice1]]
                if vertice2 not in edges_check:
                    continue
                for edge in self.graph[vertice1]:
                    if vertice2 == edge.dest and edge.hasOut:
                        # print("=====")
                        tempWay = Way(
                            vertice1,
                            vertice2,
                            [vertice1, vertice2],
                            edge.weight,
                            hasOut=edge.diemdohang,
                        )
                        baseLine.append(tempWay)
                        outfile.write(str(tempWay.__dict__) + "\n")
        outfile.close()
        print("Tạo thành công tập đường cơ sở và lưu vào file baseLine.txt")

    def create_Simple_egde(self):
        for vertice in self.graph.keys():
            self.h[vertice] = 1
            for edge in self.graph[vertice]:
                if edge.dest > 67:
                    self.adjac_lis[vertice].append((edge.dest, edge.weight))

    def a_star_algorithm(self, start, stop):
        # In this open_lst is a lisy of nodes which have been visited, but who's
        # neighbours haven't all been always inspected, It starts off with the start
        # node
        # And closed_lst is a list of nodes which have been visited
        # and who's neighbors have been always inspected
        open_lst = set([start])
        closed_lst = set([])

        # poo has present distances from start to all other nodes
        # the default value is +infinity
        poo = {}
        poo[start] = 0

        # par contains an adjac mapping of all nodes
        par = {}
        par[start] = start

        while len(open_lst) > 0:
            n = None
            # print(convertWay(open_lst))
            # it will find a node with the lowest value of f() -
            for v in open_lst:
                if n == None or poo[v] + self.h[v] < poo[n] + self.h[n]:
                    n = v

            if n == None:
                print("Path does not exist!")
                return None

            # if the current node is the stop
            # then we start again from start
            if n == stop:
                reconst_path = []

                while par[n] != n:
                    reconst_path.append(n)
                    n = par[n]

                reconst_path.append(start)

                reconst_path.reverse()

                # print("Path found: {}".format(convertWay(reconst_path)))
                return reconst_path

            # for all the neighbors of the current node do
            for (m, weight) in self.get_neighbors(n):
                # if the current node is not presentin both open_lst and closed_lst
                # add it to open_lst and note n as it's par
                if m not in open_lst and m not in closed_lst:
                    # print(n, m)
                    open_lst.add(m)
                    par[m] = n
                    poo[m] = poo[n] + weight

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update par data and poo data
                # and if the node was in the closed_lst, move it to open_lst
                else:
                    if poo[m] > poo[n] + weight:
                        poo[m] = poo[n] + weight
                        par[m] = n

                        if m in closed_lst:
                            closed_lst.remove(m)
                            open_lst.add(m)

            # remove n from the open_lst, and add it to closed_lst
            # because all of his neighbors were inspected
            open_lst.remove(n)
            closed_lst.add(n)

        print("Path does not exist!")
        return None
