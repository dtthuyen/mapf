import numpy as np
from utils import convertWay, load_map_to_list, mPoint, pMatrixInt

start_row = 6
end_row = 64
start_col = 10
end_col = 62
dimensions = 70
#output
out = []
for x in range(start_row, end_row, 3):
    for y in range(start_col, end_col, 3):
        out.append([x, y])
np.savetxt("arrOutput.csv", out, fmt="%s", delimiter=",")

#input
inPoint = []
for x in range(start_row, end_row, 3):
    if x == 33:
        inPoint.append([x,dimensions])
        continue
    if x == 36:
        inPoint.append([x,2])
        continue
    inPoint.append([x,2])
    inPoint.append([x,dimensions])
np.savetxt("arrInput.csv", inPoint, fmt="%s", delimiter=",")

#back
back = []
for x in range(5, 64, 3):
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

# #point total
# intersect = []

# np.savetxt("arrPointTotal.csv", intersect, fmt="%s", delimiter=",")

#find queue
map_rows = load_map_to_list('map.csv')
arrQueue = []
num_rows = None
num_cols = None
for i in range(1, 69):
    for j in range(1, dimensions+1):
        if j == 1:
            continue
        location = mPoint(i, j)
        direct = map_rows[location - 1]
        if direct == 'q':
            arrQueue.append([i, j])
np.savetxt(csv_source + "arrQueue.csv", arrQueue, fmt="%s", delimiter=",")




