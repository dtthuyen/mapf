import base64
import sys
import zlib

wayStr = "[[1,34],[1,36], [1, 39], [1, 42], [1, 48], [1, 50], [1, 51], [16, 51], [21, 51], [34, 51], [34, 50], [34, 47], [34, 42], [34, 39], [34, 36], [34, 31], [34, 30], [34, 25], [34, 22], [34, 19], [34, 14], [34, 13], [34, 8], [34, 5], [34, 2], [21, 2], [16, 2], [1, 2], [1, 5], [1, 8], [1, 13], [1, 14], [16, 14], [16, 13], [16, 8]]".replace(
    " ", ""
)

print(wayStr)
print("size of original way is: ", sys.getsizeof(wayStr))

print("base64 string compression: ", sys.getsizeof(wayStr.encode("ascii")))
# newWay = zlib.compress(wayStr)
# print("size after compress is: ", sys.getsizeof(newWay))

from smaz import compress, decompress

print(compress("Hello, world!"))

newWay = compress(wayStr)
print("size after compress is: ", sys.getsizeof(newWay))
