from utils import (loadPointPort)
day = "040122"
csv_folder = f"csv{day}/"
arrCross_path = csv_folder + "arrPointTotal.csv"
arrCross = loadPointPort(arrCross_path)
print(len(arrCross))
# a = list(set(arrCross))
print(set(arrCross))