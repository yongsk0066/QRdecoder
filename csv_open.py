# f = open('ver_align.csv', 'r')
# file = f.readlines()
# version = 2
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

# for line in file:
#     align_position_dict[version] = list(map(lambda x: int(x), line.strip().split(",")))
#     # print(list(map(lambda x : int(x), line.strip().split(","))))
#     version += 1
# print(align_position_dict)
#
# start = 6
# last = lambda x: x - 6

# def get_width(version):
#     return 20 + (version - 1) * 4
#
#
# def get_align_position(version):
#     # last(get_width(version))
#     return [start]
#
#
# for i in range(7, 41):
#     lst = get_align_position(i)
#     version_type = i // 7 + 1
#     delta = (last(get_width(i)) - lst[0]) // version_type
#     lst_val = start
#     # print(i//7 + 1)
#     if version_type != 1:
#         # print(version_type)
#         for j in range(0, version_type - 1):
#             lst.append(lst_val + delta)
#             lst_val += delta
#         lst.append(last(get_width(i)))
#
#     print(lst)
#     # print(get_width(i), lst, delta+6)
