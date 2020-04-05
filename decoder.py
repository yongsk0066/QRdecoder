from PIL import Image
import numpy as np
from excel_painter import paint_qrcode_to_excel

EC_LEVEL = {"11": "L", "10": "M", "01": "Q", "00": "H"}
align_position_dict = {2: [6, 18],
                       3: [6, 22],
                       4: [6, 26],
                       5: [6, 30],
                       6: [6, 34],
                       7: [6, 22, 38],
                       8: [6, 24, 42],
                       9: [6, 26, 46],
                       10: [6, 28, 50],
                       11: [6, 30, 54],
                       12: [6, 32, 58],
                       13: [6, 34, 62],
                       14: [6, 26, 46, 66],
                       15: [6, 26, 48, 70],
                       16: [6, 26, 50, 74],
                       17: [6, 30, 54, 78],
                       18: [6, 30, 56, 82],
                       19: [6, 30, 58, 86],
                       20: [6, 34, 62, 90],
                       21: [6, 28, 50, 72, 94],
                       22: [6, 26, 50, 74, 98],
                       23: [6, 30, 54, 78, 102],
                       24: [6, 28, 54, 80, 106],
                       25: [6, 32, 58, 84, 110],
                       26: [6, 30, 58, 86, 114],
                       27: [6, 34, 62, 90, 118],
                       28: [6, 26, 50, 74, 98, 122],
                       29: [6, 30, 54, 78, 102, 126],
                       30: [6, 26, 52, 78, 104, 130],
                       31: [6, 30, 56, 82, 108, 134],
                       32: [6, 34, 60, 86, 112, 138],
                       33: [6, 30, 58, 86, 114, 142],
                       34: [6, 34, 62, 90, 118, 146],
                       35: [6, 30, 54, 78, 102, 126, 150],
                       36: [6, 24, 50, 76, 102, 128, 154],
                       37: [6, 28, 54, 80, 106, 132, 158],
                       38: [6, 32, 58, 84, 110, 136, 162],
                       39: [6, 26, 54, 82, 110, 138, 166],
                       40: [6, 30, 58, 86, 114, 142, 170]}


class QR:
    def __init__(self, src):
        self._img = Image.open(src).convert('RGB')
        self.ec = None
        self.mask = None
        self.mask_func = None
        self.mask_array = None
        self.array = None
        self.width = None
        self.__initialize()

    def __initialize(self):
        self.__make_nparray()
        self.__get_width()
        self.__get_version()
        self.__get_ec()
        self.__get_mask_pattern()
        self.__get_mask_array()

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

    def __get_positions(self):
        width = self.width - 1
        p_width = 8
        gap_width = width - p_width - 1

        left_top = [[0, 0], [p_width, p_width]]
        left_bottom = [[gap_width, 0], [width, p_width]]
        right_top = [[0, gap_width], [p_width, width]]
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

    def __is_mask(self, i, j):
        return self.__is_timing(i, j) or self.__is_position(i, j) or self.__is_align(i, j)

    def __get_mask_array(self):
        width = self.width
        array = np.zeros((width, width))
        # print(array[0][0], array[width - 1][width - 1])
        for i in range(0, width):
            for j in range(0, width):
                if not self.__is_mask(i, j):
                    array[i][j] = 1 if self.mask_func(i, j) else 0

        self.mask_array = array

    def xor_array(self):
        return np.logical_xor(self.array, self.mask_array)


qrcode = QR("o2o_qrcode.png")
