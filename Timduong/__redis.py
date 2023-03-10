# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 09:38:46 2021

@author: kyo
"""

import json
import time

import redis

r = redis.Redis(host="127.0.0.1", port=6379, db=4, password="")
rb = redis.Redis(host="127.0.0.1", port=6379, db=5, password="")


def set_coordinate_to_redis(path, start, end):
    key = str(start) + "," + str(end)
    json_arr = list()
    for point in path:
        temp = {"x": point[0], "y": point[1]}
        json_arr.append(temp)
    json_arr = json.dumps(json_arr)
    r.set(key, json_arr)


def set_coordinate_wayBack_to_redis(path, start, end):
    key = str(start) + "," + str(end)
    json_arr = list()
    for point in path:
        temp = {"x": point[0], "y": point[1]}
        # temp = point
        json_arr.append(temp)
    json_arr = json.dumps(json_arr)
    rb.set(key, json_arr)
