import numpy as np
out = []
for x in range(6, 66, 3):
    for y in range(9, 63, 3):
        out.append([x, y])
np.savetxt("arrOutput.csv", out, fmt="%s", delimiter=",")
