from PIL import Image
import numpy as np
import cv2
import math


def get_hsv_int(hsv):
    return tuple((int(round(hsv[0] * 360)), int(round(hsv[1] * 100)), int(round(hsv[2] * 100))))


def hsv_to_rgb(hsv):
    import colorsys
    rgb = colorsys.hsv_to_rgb(hsv[0] / 360, hsv[1] / 100, hsv[2] / 100)
    return tuple(map(lambda x: int(x * 255), rgb))


def rgb_to_hsv(rgb):
    import colorsys
    hsv = colorsys.rgb_to_hsv(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)
    return get_hsv_int(hsv)


def tuple_to_string(tp):
    return f'({tp[0]:3},{tp[1]:3},{tp[2]:3})'


def BGR2RGB(bgr):
    """
    :param BGR: tuple
    :return: RGB (R,G,B)
    """
    return bgr[2], bgr[1], bgr[0]


def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst


def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


def merge_image_list(mode, img_list):
    dst = Image.new(mode, (img_list[0].width, img_list[0].height * len(img_list)))
    for i in range(0, len(img_list)):
        dst.paste(img_list[i], (0, i * img_list[i].height))

    return dst


def get_scale(min, max, scale):
    gap = (max - min) / (scale - 1)
    return list(map(lambda x: round(x * gap), range(0, scale)))


def get_scale_left(min, max, scale):
    gap = (max - min) / scale
    return list(map(lambda x: round(x * gap), range(0, scale)))


def closest(lst, K):
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - K))]


h_list = get_scale_left(0, 360, 30)
sv_list = get_scale(0, 100, 15)


def convert_close_hsv(hsv):
    h = closest(h_list, hsv[0])
    s = closest(sv_list, hsv[1])
    v = closest(sv_list, hsv[2])
    return h, s, v

def rgb_2_close_rgb(rgb):
    return hsv_to_rgb(convert_close_hsv(rgb_to_hsv(rgb)))


def image_to_palette(src, K=10):
    img = Image.open(src).convert('RGB')

    # resize
    # width = math.floor(size * img.size[0] / img.size[1])
    # img = img.resize((width, size))

    img_arr = np.asarray(img)

    Z = img_arr.reshape((-1, 3))

    # convert to np.float32
    Z = np.float32(Z)

    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = K
    ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Now convert back into uint8, and make original image
    # center = np.uint8(center)
    re_center = np.uint8(list(map(lambda x: rgb_2_close_rgb(x), center)))

    # show
    re_res = re_center[label.flatten()]
    # res = center[label.flatten()]

    # res2 = res.reshape((img.size[1], img.size[0], 3))
    re_res2 = re_res.reshape((img.size[1], img.size[0], 3))

    # img = Image.fromarray(res2).show()
    img = Image.fromarray(re_res2).show()


    img_list = []
    hsv_list = []
    color_list = [[], []]
    h_list = [(48, 93, 100), (204, 50, 50), (264, 50, 93), (204, 43, 71), (60, 57, 100), (204, 7, 86), (264, 36, 93),
              (48, 64, 86), (36, 50, 64), (204, 29, 79)]
    # print(center)
    for each_img in center:
        color_list[0].append(rgb_to_hsv(each_img))
        color_list[1].append(tuple((each_img[0], each_img[1], each_img[2])))
        hsv_list.append(Image.new('RGB', (500, 100), hsv_to_rgb(rgb_to_hsv(each_img))))
        img_list.append(Image.new('RGB', (500, 100), (each_img[0], each_img[1], each_img[2])))
        # print(rgb_to_hsv(each_img))
    test_list = list(map(lambda x: Image.new('RGB', (500, 100), hsv_to_rgb(convert_close_hsv(x))), color_list[0]))
    im1 = merge_image_list('RGB', img_list)
    im2 = merge_image_list('RGB', hsv_list)
    im3 = merge_image_list('RGB', test_list)

    get_concat_h(get_concat_h(im1, im2), im3).show()

    # print(color_list[0])

    # for i in range(0, 10):
    #     print(f'hsv:{tuple_to_string(color_list[0][i])} rgb:{tuple_to_string(color_list[1][i])}')

    # Image.new('RGB', (500, 100), (BGR2RGB(center[0])))
    # Image.new('RGB', (500, 500), (center[1][2], center[1][1], center[1][0])).show()
    # cv2.imshow('res2',res2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    palette = re_center
    return palette


a = image_to_palette('image_test.jpg', K=20)
# print(a)
import json
b = json.dumps(a.tolist())
print(type(b))


