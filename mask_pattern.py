"""
mask pattern type ( 0 ~ 7 )


"""


def get_mask_pattern(mask_type):
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
