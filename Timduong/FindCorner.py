import numpy as np

from utils import convertWay, load_map_to_list, mPoint, pMatrixInt


day = "070222"
csv_source = "csv" + day + "/"
csv_map_file = csv_source + "map350_{}_X.csv".format(day)

map_rows = load_map_to_list(csv_map_file)

arrCorner = []

num_rows = None
num_cols = None

for i in range(1, 69):
    for j in range(1, 69):
        if j == 1:
            continue
        location = mPoint(i, j)
        print(f"xet diem {(i, j)}")
        direct = map_rows[location - 1]
        # if (i, j) != (46, 63):
        #     # print(direct)
        #     continue
        # if direct == 'q':
        #     print("diem queue: ", (i, j))
        if len(direct) > 1 or direct == "x" or direct == "q":
            continue
        else:
            # print("xet diem {} and direct {}".format((i, j), direct))
            if direct == "u":
                nex_direct = map_rows[mPoint(i, j - 1) - 1]
                if nex_direct != direct and len(nex_direct) == 1:
                    arrCorner.append([i, j - 1])
                    print("them diem goc: ", [i, j - 1])
            elif direct == "d":
                nex_direct = map_rows[mPoint(i, j + 1) - 1]
                if nex_direct != direct and len(nex_direct) == 1:
                    arrCorner.append([i, j + 1])
                    print("them diem goc: ", [i, j + 1])
            elif direct == "r":
                nex_direct = map_rows[mPoint(i + 1, j) - 1]
                if nex_direct != direct and len(nex_direct) == 1:
                    arrCorner.append([i + 1, j])
                    print("them diem goc: ", [i + 1, j])

            elif direct == "l":
                nex_direct = map_rows[mPoint(i - 1, j) - 1]
                if nex_direct != direct and len(nex_direct) == 1:
                    arrCorner.append([i - 1, j])
                    print("them diem goc: ", [i - 1, j])
            else:
                print("diem loi ", (i, j), "direct: ", direct)
            # print("=========================================================")

np.savetxt(csv_source + "arrCorner.csv", arrCorner, fmt="%s", delimiter=",")
