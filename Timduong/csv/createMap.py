import numpy as np
from utils import convertWay, load_map_to_list, mPoint, pMatrixInt

start_row = 6
end_row = 64
start_col = 9
end_col = 61
dimensions_width = 68
dimensions_height = 68

#input
inPoint = []
for x in range(start_row, end_row, 3):
    if x == 33:
        inPoint.append([x,dimensions_height])
        continue
    if x == 36:
        inPoint.append([x,2])
        continue
    inPoint.append([x,2])
    inPoint.append([x,dimensions_height])
np.savetxt("arrInput.csv", inPoint, fmt="%s", delimiter=",")

#back
back = []
for x in range(start_row-1, end_row+1, 3):
    back.append([x,2])
    back.append([x,dimensions])
np.savetxt("arrBack.csv", back, fmt="%s", delimiter=",")

#delivery
delivery = []
for x in range(5, 65, 1):
    if x in range(start_row, end_row,3):
        delivery.append([x,start_col - 1])
        delivery.append([x,end_col])
        continue
    for y in range(start_col, end_col, 3):
        delivery.append([x,y])
np.savetxt("arrDelivery.csv", delivery, fmt="%s", delimiter=",")

#input to delivery
arrI2D = []
for _in in inPoint:
    for _deliver in delivery:
        arrI2D.append(f"\"{','.join(str(x) for x in _in)}\",\"{','.join(str(x) for x in _deliver)}\"")
np.savetxt("IP2DeliveryWay.csv", arrI2D, fmt="%s", delimiter=",")

# #corner
# corner = []
# np.savetxt("arrCorner.csv", corner, fmt="%s", delimiter=",")


map_rows = load_map_to_list('map.csv')
arrQueue = [] 
arrOutput = [] 
arrPoint = []
for i in range(1, 69):
    for j in range(1, 69):
        if j == 1:
            continue
        location = mPoint(i, j)
        direct = map_rows[location - 1]
        if direct == 'q': #find queue
            arrQueue.append([i, j])
        if direct == 'x': #find Output
            arrOutput.append([i, j])
        if len(direct) > 2: #find point
            arrPoint.append([i, j])
np.savetxt("arrQueue.csv", arrQueue, fmt="%s", delimiter=",")
np.savetxt("arrOutput.csv", arrOutput, fmt="%s", delimiter=",")
np.savetxt("arrPoint.csv", arrPoint, fmt="%s", delimiter=",")




