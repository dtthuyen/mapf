import numpy as np

from utils import convertWay, load_map_to_list, mPoint, pMatrixInt


day = "040122"
csv_source = "csv" + day + "/"
csv_map_file = csv_source + "map350_{}_X.csv".format(day)

map_rows = load_map_to_list(csv_map_file)

arrQueue = []

num_rows = None
num_cols = None

for i in range(1, 69):
    for j in range(1, 69):
        if j == 1:
            continue
        location = mPoint(i, j)
        print(f"xet diem {(i, j)}")
        direct = map_rows[location - 1]
        if direct == 'q':
            arrQueue.append([i, j])

np.savetxt(csv_source + "arrQueue.csv", arrQueue, fmt="%s", delimiter=",")
