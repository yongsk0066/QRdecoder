from PIL import Image
import numpy as np

img = Image.open('o2o_qrcode.png').convert('RGB')
img_arr = np.asarray(img)[:,:,0]
