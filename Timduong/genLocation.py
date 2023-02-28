import csv

import numpy as np
from tqdm import tqdm

from utils import xytoStr

day = "040122"
csv_source = "csv" + day + "/"
csv_map_file = csv_source + "map350_{}_X.csv".format(day)

IOway = open(csv_map_file)
IOway = csv.reader(IOway, delimiter=",")
list_IOway = []
arrInput = []
arrOutput = []
arrCharge = []
arrPoint = []
row_index = 1
for row in IOway:
    if row_index == 1:
        row_index += 1
        continue
    else:
        print(row)
        for i, ele in enumerate(row):
            if len(ele) > 1:
                arrPoint.append([i + 1, row_index])
            if ele == "1":
                arrOutput.append([i + 1, row_index])
            elif ele == "2":
                arrInput.append([i + 1, row_index])
            elif ele == "3":
                arrCharge.append([i + 1, row_index])
        row_index += 1
# np.savetxt("arrOutput.csv", arrOutput, fmt="%s", delimiter=",")
# np.savetxt("arrInput.csv", arrInput, fmt="%s", delimiter=",")
# np.savetxt("arrCharge.csv", arrCharge, fmt="%s", delimiter=",")
print("num of cross point: ", len(arrPoint))
np.savetxt(csv_source + "arrPoint.csv", arrPoint, fmt="%s", delimiter=",")
