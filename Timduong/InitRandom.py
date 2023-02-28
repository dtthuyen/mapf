from utils import load_map_to_list, loadPointPort, mPoint, pMatrixInt
import random as rd
import numpy as np

InitPoint = []


print("=================== Load tất cả các file cần thiết ===========================")
day = "040122"
csv_folder = f"csv{day}/"
map_path = csv_folder + f"map350_{day}_X.csv"
arrIP_path = csv_folder + "arrInput.csv"
arrCross_path = csv_folder + "arrPointTotal.csv"
arrOP_path = csv_folder + "arrOutput.csv"
arrCorner_path = csv_folder + "arrCorner.csv"
IO_path_file = csv_folder + "IP2OPway.csv"
IDelivery_path_file = csv_folder + "IP2DeliveryWay.csv"
arrBack_path = csv_folder + "arrBack.csv"
arrDelivery_path = csv_folder + "arrDelivery.csv"

map_rows = load_map_to_list(map_path)


arrIP = loadPointPort(arrIP_path)
arrOutport = loadPointPort(arrOP_path)

while len(InitPoint) < 400:
    rand_location = [rd.randint(5, 64), rd.randint(9, 60)]
    if rand_location in arrOutport or rand_location in arrIP:
        continue
    direct_location = mPoint(rand_location[0], rand_location[1])
    direct = map_rows[direct_location-1]
    if direct != "q":
        InitPoint.append(rand_location)

print("num of init point: ", len(InitPoint))
np.savetxt(csv_folder + "arrInit.csv", InitPoint, fmt="%s", delimiter=",")

