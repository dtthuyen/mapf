# -*- coding: utf-8 -*-
import datetime
import time

from mysql.connector import Error, MySQLConnection

# import pymysql.cursors
# import csv
# import numpy as np
# import os

# connect database.
def connect():
    """Kết nối MySQL bằng module MySQLConnection"""
    db_config = {
        "host": "localhost",
        "database": "agv350",
        "user": "root",
        "password": "",
    }

    # Biến lưu trữ kết nối
    conn = None

    try:
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            return conn

    except Error as error:
        print(error)

    return conn


# Test thử
conn = connect()
print(conn)


def showOne():
    # Phương thức fetchone() sẽ trả về row dữ liệu tiếp theo trong kết quả trả về, hoặc trả về None nếu kết quả là rỗng.
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM agv")
        row = cursor.fetchone()

        while row is not None:
            print(row)
            row = cursor.fetchone()

    except Error as e:
        print(e)

    finally:
        # Đóng kết nối
        cursor.close()
        conn.close()


# showOne()
def showAll():
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM agv")
        rows = cursor.fetchall()
        print("Total Row(s):", cursor.rowcount)
        for row in rows:
            print(row)

    except Error as e:
        print(e)

    finally:
        # Đóng kết nối
        cursor.close()
        conn.close()


# showAll()
def iter_row(cursor, size=10):
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row


def showLim(lim=10):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM agv")
        for row in iter_row(cursor, lim):
            print(row)

    except Error as e:
        print(e)

    finally:
        # Đóng kết nối
        cursor.close()
        conn.close()


# showLim()


def insertAgv(name, status):
    query = "INSERT INTO agv(name,status) " "VALUES(%s,%s)"
    args = (name, status)
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(query, args)
        if cursor.lastrowid:
            print("AGV ID insert:", cursor.lastrowid)
        else:
            print("Insert false!!")
        conn.commit()
    except Error as error:
        print(error)

    finally:
        # Đóng kết nối
        cursor.close()
        conn.close()


def creatByTime():
    dt_now = datetime.datetime.now()
    out = (
        str(dt_now.year)
        + str(dt_now.month)
        + str(dt_now.day)
        + str(dt_now.hour)
        + str(dt_now.minute)
        + str(dt_now.second)
        + str(dt_now.microsecond)
    )
    return out


# agvName = creatByTime()
# insertAgv(agvName, "Active")
def updateAgv(agvname, status):
    # Câu lệnh update dữ liệu
    query = """ UPDATE agv
                SET status = %s
                WHERE name = %s """

    data = (status, agvname)

    try:
        # Kết nối database
        conn = connect()

        # Cập nhật tiêu đề
        cursor = conn.cursor()
        cursor.execute(query, data)

        # Chấp nhận sự thay đổi
        conn.commit()

    except Error as error:
        print(error)

    finally:
        # Đóng kết nối
        cursor.close()
        conn.close()


# print (agvName)
# updateAgv("20219259556918638", "Delivery")
# Status = IDE, Active, Waiting, Delivery, Return, Error
def deleteAvg(agvid, agvname):
    query = "DELETE FROM agv WHERE id = %s or name = %s"

    try:
        conn = connect()

        # Thực thi câu truy vấn
        cursor = conn.cursor()
        cursor.execute(
            query,
            (
                agvid,
                agvname,
            ),
        )

        # Chấp nhận sự thay đổi
        conn.commit()

    except Error as error:
        print(error)

    finally:
        # Đóng kết nối
        cursor.close()
        conn.close()


# deleteAvg(0,"20219259558393177") ko co id 0 nen se xoa theo ten
# deleteAvg(3,"") ko co ten nen xoa theo id
def emptyTable(tableName):
    #    query = "LOCK TABLE %s WRITE; TRUNCATE %s; UNLOCK TABLES;"
    query = "TRUNCATE TABLE " + str(tableName)
    try:
        conn = connect()
        cursor = conn.cursor()
        #        cursor.execute(query,(tableName,tableName,))
        cursor.execute(query)
        conn.commit()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()


# emptyTable("map_default")
# khoi tao
# INSERT INTO `map_default` (`id`, `name`, `path`, `note`) VALUES (NULL, 'Default4', '4,3\r\n2, 3\r\n2, 16\r\n5, 16\r\n5, 5\r\n8, 5\r\n8, 16\r\n11, 16\r\n11, 5\r\n14, 5\r\n14, 16\r\n17, 16\r\n17, 3', 'duong di tu vi tri xp so 1: (4,3)');
def showMapDefault(param="Default2"):
    # Phương thức fetchone() sẽ trả về row dữ liệu tiếp theo trong kết quả trả về, hoặc trả về None nếu kết quả là rỗng.
    query = "SELECT path FROM map_default WHERE name='" + str(param) + "'"
    # print (query)
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        # print (row)
        return row
    except Error as e:
        print(e)

    finally:
        # Đóng kết nối
        cursor.close()
        conn.close()


# outP = showMapDefault("Default9")
# print (type(outP))
# tuple
# print(outP[0])
# arrStr = outP[0].split('\r\n')
# print(arrStr)
# print (outP)
# showOne()
def insertColor(name, rgb, hex16):
    query = "INSERT INTO color(name,rgb,hex16) " "VALUES(%s,%s,%s)"
    args = (name, rgb, hex16)
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(query, args)
        if cursor.lastrowid:
            print("Color ID insert:", cursor.lastrowid)
        else:
            print("Insert false!!")
        conn.commit()
    except Error as error:
        print(error)

    finally:
        # Đóng kết nối
        cursor.close()
        conn.close()


def insertPackage(name, inport, outport, color):
    query = "INSERT INTO package(name,inport,outport,color) " "VALUES(%s,%s,%s,%s)"
    args = (name, inport, outport, color)
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(query, args)
        if cursor.lastrowid:
            print("Package ID insert:", cursor.lastrowid)
        else:
            print("Insert false!!")
        conn.commit()
    except Error as error:
        print(error)

    finally:
        # Đóng kết nối
        cursor.close()
        conn.close()


def calMap():
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name_agv,path FROM map WHERE done=0 ")
        rows = cursor.fetchall()
        print("Total Row(s):", cursor.rowcount)
        for row in rows:
            print(row)
        return rows

    except Error as e:
        print(e)

    finally:
        # Đóng kết nối
        cursor.close()
        conn.close()


# calMap()
def showColor():
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name,rgb,hex16 FROM color")
        rows = cursor.fetchall()
        print("Total Row(s):", cursor.rowcount)
        return rows

    except Error as e:
        print(e)

    finally:
        # Đóng kết nối
        cursor.close()
        conn.close()


# showColor()


def showTable(table):
    try:
        conn = connect()
        cursor = conn.cursor()
        query = "SELECT id,path,cost FROM " + table
        cursor.execute(query)
        rows = cursor.fetchall()
        print("Total Row(s):", cursor.rowcount)
        return rows

    except Error as e:
        print(e)

    finally:
        # Đóng kết nối
        cursor.close()
        conn.close()


def updateCost(table, idk, result):
    # Câu lệnh update dữ liệu
    # query = """ UPDATE %s
    #            SET status = ""
    #            WHERE id = %s """
    sttime = "\r\n".join(str(x) for x in result[1])
    query = (
        "UPDATE "
        + table
        + " SET cost ="
        + str(result[0])
        + ',time = "'
        + sttime
        + '" WHERE id ='
        + str(idk)
    )
    print(query)
    # data = (table, id)
    try:
        conn = connect()
        cursor = conn.cursor()
        # cursor.execute(query, data)
        cursor.execute(query)
        conn.commit()

    except Error as error:
        print(error)

    finally:
        # Đóng kết nối
        cursor.close()
        conn.close()


def updateMapDetail(table, idk, result):
    stp = "\r\n".join(str(x) for x in result)
    stpn = stp.replace("[", "")
    stp = stpn.replace("]", "")
    query = "UPDATE " + table + ' SET pdetail = "' + stp + '" WHERE id =' + str(idk)
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()

    except Error as error:
        print(error)

    finally:
        # Đóng kết nối
        cursor.close()
        conn.close()


def importWay(table, name, path, pdetail, cost, key, include):
    query = (
        "INSERT INTO " + table + " (name,path,pdetail,cost) "
        "VALUES(%s,%s,%s,%s,%s,%s)"
    )
    args = (name, path, pdetail, cost, key, include)
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(query, args)
        if cursor.lastrowid:
            print("Package ID insert:", cursor.lastrowid)
        else:
            print("Insert false!!")
        conn.commit()
    except Error as error:
        print(error)

    finally:
        # Đóng kết nối
        cursor.close()
        conn.close()


# importWay("map_default","abcddddd","path","fsdsfsdfs","0")
# sq.importTempWay(name,sW1,sW2,str(dist[goal]),pMatrixStr(source),pMatrixStr(goal),haveOut)
conn = connect()


def importTempWay(name, path, path1d, pdetail, cost, start, end, goal):
    query = (
        "INSERT INTO map_temp( name, path, path1d, pdetail,cost,start,end,goal)"
        "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
    )
    args = (name, path, path1d, pdetail, cost, start, end, goal)
    cursor = conn.cursor()
    try:
        cursor = conn.cursor()
        cursor.execute(query, args)
        if cursor.lastrowid:
            pass
            # print("Package ID insert:", cursor.lastrowid)
        else:
            print("Insert false!!")
        conn.commit()

    except Error as error:
        print(error)
    # cursor.close()
    # conn.close()


def importWayBack(name, path, pdetail, cost, start, end, goal):
    query = (
        "INSERT INTO map_wayback( name, path, pdetail,cost,start,end,goal)"
        "VALUES(%s,%s,%s,%s,%s,%s,%s)"
    )
    conn = connect()

    args = (name, path, pdetail, cost, start, end, goal)
    try:
        cursor = conn.cursor()
        cursor.execute(query, args)
        if cursor.lastrowid:
            print("Package ID insert:", cursor.lastrowid)
        else:
            pass
            # print("Insert false!!")
        conn.commit()

    except Error as error:
        print(error)
    finally:
        # Đóng kết nối
        cursor.close()
        conn.close()


def saveErr(start, end, goal):
    # listOut = [start,end,goal]
    # np.savetxt("errorLog.csv", listOut, fmt='%s', delimiter=",")
    query = "INSERT INTO errorlog(start,end,goal)" "VALUES(%s,%s,%s)"
    args = (start, end, goal)
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(query, args)
        if cursor.lastrowid:
            print("Err ID insert:", cursor.lastrowid)
        else:
            # print (path,pdetail,cost,start,end,goal)
            print("Insert log false!!")
        conn.commit()
    except Error as error:
        print(error)

    finally:
        # Đóng kết nối
        cursor.close()
        conn.close()

    return 1


def importSubWay2(name, path, pdetail, cost, start, end, goal):
    query = (
        "INSERT INTO map_wayback(path, pdetail,cost,start,end,goal)"
        "VALUES(%s,%s,%s,%s,%s,%s)"
    )
    # print(query)
    args = (path, pdetail, cost, start, end, goal)
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(query, args)
        if cursor.lastrowid:
            print("SubMap ID insert:", cursor.lastrowid)
        else:
            # print (path,pdetail,cost,start,end,goal)
            saveErr(start, end, goal)
            print("Insert sub false!!")
        conn.commit()
    except Error as error:
        print(error)

    finally:
        # Đóng kết nối
        cursor.close()
        conn.close()
