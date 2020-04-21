from PIL import Image
import numpy as np
import position_data
from excel_painter import paint_qrcode_to_excel

EC_LEVEL = {"11": "L", "10": "M", "01": "Q", "00": "H"}
MODE_INDICATOR = {"0001": "Numeric Mode", "0010": "Alphanumeric Mode",
                  "0100": "Byte Mode", "1000": "Kanji Mode", "0111": "ECI Mode"}
align_position_dict = position_data


class QR:
    def __init__(self, src):
        self._img = Image.open(src).convert('RGB')
        self.ec = None
        self.array = None
        self.mask = None
        self.mask_func = None
        self.mask_array = None
        self.xor_array = None
        self.width = None
        self.mode = None
        self.__initialize()

    def __initialize(self):
        self.__make_nparray()
        self.__get_width()
        self.__get_version()
        self.__get_ec()
        self.__get_mask_pattern()
        self.__get_mask_array()
        self.__get_xor_array()
        # self.__get_mode_indicator()

    def __make_nparray(self):
        img_arr = np.asarray(self._img)[:, :, 0]
        vfunc = np.vectorize(lambda x: 1 if x == 0 else 0)
        self.array = vfunc(img_arr)

    def __get_width(self):
        self.width = len(self.array)

    def __get_version(self):
        self.version = (self.width - 21) // 4 + 1

    def __get_ec(self):
        self.ec = EC_LEVEL["".join(map(str, self.array[8][:2]))]

    def __get_mask_pattern(self):
        self.mask = "".join(map(str, self.array[8][2:5]))
        self.mask_func = self.__mask_pattern(self.mask)

    def __mask_pattern(self, mask_type):
        if mask_type == "111":
            return lambda i, j: j % 3 == 0
        elif mask_type == "110":
            return lambda i, j: (i + j) % 3 == 0
        elif mask_type == "101":
            return lambda i, j: (i + j) % 2 == 0
        elif mask_type == "100":
            return lambda i, j: i % 2 == 0
        elif mask_type == "011":
            return lambda i, j: ((i * j) % 3 + (i * j)) % 2 == 0
        elif mask_type == "010":
            return lambda i, j: ((i * j) % 3 + i + j) % 2 == 0
        elif mask_type == "001":
            return lambda i, j: (i // 2 + j // 3) % 2 == 0
        elif mask_type == "000":
            return lambda i, j: (i * j) % 2 + (i * j) % 3 == 0

    def __is_in_area(self, curr, area):
        if curr[0] in range(area[0][0], area[1][0] + 1) and curr[1] in range(area[0][1], area[1][1] + 1):
            return True
        else:
            return False

    def __get_positions(self, type="v"):
        width = self.width - 1
        p_width = 8
        gap_width = width - p_width
        if type != "v":
            v1 = [[gap_width - 2, 0], [gap_width, 5]]
            v2 = [[0, gap_width - 2], [5, gap_width]]
            return [v1, v2]

        left_top = [[0, 0], [p_width, p_width]]
        left_bottom = [[gap_width + 1, 0], [width, p_width]]
        right_top = [[0, gap_width + 1], [p_width, width]]
        return [left_top, left_bottom, right_top]

    def __align_range(self, location):
        return [[location[0] - 2, location[1] - 2], [location[0] + 2, location[1] + 2]]

    def __version_align_position(self):
        from itertools import product
        aligns = align_position_dict[self.version]
        all_position = list(product(aligns, aligns))
        for item in [(6, 6), (aligns[-1], 6), (6, aligns[-1])]:
            all_position.remove(item)
        return all_position

    def __is_position(self, i, j):
        position = self.__get_positions()
        for area in position:
            if self.__is_in_area([i, j], area):
                return True
        return False

    def __is_align(self, i, j):
        position = self.__version_align_position()
        for location in position:
            if self.__is_in_area([i, j], self.__align_range(location)):
                return True
        return False

    def __is_timing(self, i, j):
        return i == 6 or j == 6

    def is_mask(self, i, j):
        return self.__is_timing(i, j) or self.__is_position(i, j) or self.__is_align(i, j)

    def is_version_info(self, i, j):
        position = self.__get_positions(type="s")
        for area in position:
            if self.__is_in_area([i, j], area):
                return True
        return False

    def is_mask_test(self, i, j):
        return self.__is_timing(i, j) or self.__is_position(i, j) or self.__is_align(i, j) or self.is_version_info(i, j)

    def __get_mask_array(self):
        width = self.width
        array = np.zeros((width, width))
        # print(array[0][0], array[width - 1][width - 1])
        for i in range(0, width):
            for j in range(0, width):
                if not self.is_mask_test(i, j):
                    array[i][j] = 1 if self.mask_func(i, j) else 0

        self.mask_array = array

    def __get_xor_array(self):
        vfunc = np.vectorize(lambda x: 1 if x else 0)
        self.xor_array = vfunc(np.logical_xor(self.array, self.mask_array))

    # def __get_mode_indicator(self):
    #     xor = self.xor_array
    #     indicator = f'{"".join(xor[-1][-2:0])}{"".join(xor[-2][-2:0])}'
    #     self.mode = MODE_INDICATOR[indicator]


qrcode2 = QR("93test.png")
qrcode = QR("o2o_2png.png")

xor = qrcode.xor_array


# indicator = f'{xor[-1][-1]}{xor[-1][-2]}{xor[-2][-1]}{xor[-2][-2]}'
# print(MODE_INDICATOR[indicator])
# print(qrcode.ec)
# print(qrcode.version)
# # paint_qrcode_to_excel(qrcode.array, "version_2_arr")
# paint_qrcode_to_excel(xor, "version_2_xor")
#
# #


def generate_matrix(width):
    l = []
    count = 0
    for i in range(0, width):
        l.append([])
        for j in range(0, width):
            l[i].append(count)
            count += 1
    return np.asarray(l)


def slice_range(width):
    output = []
    width_list = list(range(width - 1, -1, -1))
    width_list.remove(6)
    i = 0
    while i < width // 2:
        index = i * 2
        output.append(width_list[index:index + 2])
        i += 1
    return output
    # return Output


def get_codeword(qr):
    flag = True
    codeword = []
    width = qr.width
    array = qr.xor_array
    x_list = slice_range(width)
    for x in x_list:
        # upward
        if flag:
            for y in range(width - 1, -1, -1):
                if not qr.is_mask_test(y, x[0]):
                    codeword.append(str(array[y][x[0]]))
                if not qr.is_mask_test(y, x[1]):
                    codeword.append(str(array[y][x[1]]))
            # turn
            flag = False

        # downward
        elif not flag:
            for y in range(0, width):
                if not qr.is_mask_test(y, x[0]):
                    codeword.append(str(array[y][x[0]]))
                if not qr.is_mask_test(y, x[1]):
                    codeword.append(str(array[y][x[1]]))
            flag = 1

    return "".join(codeword)


print(qrcode.ec, qrcode.mask)
result = get_codeword(qrcode)
print(MODE_INDICATOR[result[:4]])
print(result[4:20])
print(int(result[4:4 + 8*16], 2))
print(result[4:4 + 8*16])
qrcode.is_version_info(0, 0)
refine_result = result
n = 8
chunks = [refine_result[i:i + n] for i in range(0, len(refine_result), n)]
print("\n".join(chunks))
data = list(map(lambda x: int(x, 2), chunks))
#
# for i in range(0, len(data[1:data[0] + 1])):
#     if data[1:data[0] + 1][i] != data2[1:data2[0] + 1][i]:
#         print(i, hex(data[1:data[0] + 1][i]), hex(data2[1:data2[0] + 1][i]))
#
# print("\n")


# print(data[0], data[1:data[0] + 1], data[data[0] + 1:])
# hex_data = list(map(lambda x: f'{x:02x}', data))
# str_data = list(map(lambda x: chr(x), data))
# print(str_data)
# print(hex_data[:44])
# print(hex_data[44:88])
# print(hex_data[88:132])
# print(hex_data[132:177])
hex_data = data
full_list = [hex_data[:44], hex_data[44:88], hex_data[88:132], hex_data[132:177]]
ll = []
for i in range(0, 44):
    ll.append(f'{full_list[0][i]} {full_list[1][i]} {full_list[2][i]} {full_list[3][i]}')
# bytearray.fromhex(x).decode()
# str_data = list(map(lambda x: chr(x), ll))
# print(str_data)
ls = " ".join(ll).split(" ")
# str_data = list(map(lambda x: chr(int(x)), ls))

print(ll)

# print(hex_data[177:222])
# print(hex_data[222:267])
# print(hex_data[267:312])
# print(hex_data[312:357])
# print(hex_data[357:402])
# print(hex_data[402:447])
# print(hex_data[447:492])
# print(hex_data[492:537])
# print(hex_data[537:582])
# print(hex_data[582:627])


# print(set(hex_data))
# for i in range(0,25):
#     print(data[i], hex_data[i])
# print(data2[0], data2[1:data2[0] + 1], data2[data2[0] + 1:])
# print(list(map(lambda x: hex(x), data2[1:data2[0] + 1])))
# def test_func(width=5):
#     data = range(width - 1, -1, - 1)
#     Inputt = iter(data)
#     length_to_split = [2] * (width // 2 + 1)
#     Output = [list(islice(Inputt, elem)) for elem in length_to_split]
#
#     array = generate_matrix(width)
#     flag = 1
#     # 1 up 0 down
#     index = 0
#
#     answer = []
#     # print(Output)
#     for x in Output:
#         if len(x) == 1:
#             break
#         if flag == 1:
#             for y in range(width - 1, -1, -1):
#                 answer.append(array[y][x[0]])
#                 answer.append(array[y][x[1]])
#             flag = 0
#         elif flag == 0:
#             for y in range(0, width):
#                 answer.append(array[y][x[0]])
#                 answer.append(array[y][x[1]])
#             flag = 1
#         index += 1
#     print(answer)
#     # print(list(range(10,-1,-1)))
#
#
# print(generate_matrix(5))
# test_func(5)
