# tool_way_VTP

# Chú thích các file dùng để tạo đường:
* `arrInput.csv` chứa tọa độ các điểm giao hàng.
* `arrOutput.csv` chứa tọa độ các điểm nhận hàng.
* `arrCorner.csv` chứa tọa độ các điểm góc.
* `arrPoint.csv` chứa tọa độ các điểm giao.
* `arrPointTotal.csv` chứa tọa độ của điểm giao và điểm góc.
* `baseLine.txt` chứa các đường cơ sở đi qua các điểm nhận hàng.
* `IP2OPway.csv` chứa tọa độ các cặp inport và outport.

## Chú ý khi tạo đường về:
* Khi xét các điểm  về của AGV thì phải thêm các điểm về này vào trong các file `arrPointTotal.csv` và `arrCorner.csv`.

# Các bước thực tạo đường

Bước 1: Dùng file `genLoaction.py` để tạo các danh sách các điểm giao nhau.

Bước 2: Dùng file `FindCorner.py` để tìm danh sách các điểm góc.


