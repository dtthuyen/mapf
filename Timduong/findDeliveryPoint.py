import numpy as np

from utils import convertWay, load_map_to_list, mPoint, pMatrixInt, loadPointPort


day = "040122"
csv_source = "csv" + day + "/"
csv_map_file = csv_source + "map350_{}_X.csv".format(day)
arrOutputFile = csv_source + "arrOutput.csv"
arrOutput = loadPointPort(arrOutputFile)
map_rows = load_map_to_list(csv_map_file)

arrDelivery = []


for point in arrOutput:
    p1 = [point[0], point[1] - 1]
    p2 = [point[0], point[1] + 1]
    p3 = [point[0] - 1, point[1]]
    p4 = [point[0] + 1, point[1]]
    if map_rows[mPoint(p1[0], p1[1]) - 1] != "q":
        arrDelivery.append(p1)

    if map_rows[mPoint(p2[0], p2[1]) - 1] != "q":
        arrDelivery.append(p2)

    if map_rows[mPoint(p3[0], p3[1]) - 1] != "q":
        arrDelivery.append(p3)

    if map_rows[mPoint(p4[0], p4[1]) - 1] != "q":
        arrDelivery.append(p4)

print("num of cross point: ", len(arrDelivery))
np.savetxt(csv_source + "arrDelivery.csv", arrDelivery, fmt="%s", delimiter=",")
