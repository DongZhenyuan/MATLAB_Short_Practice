import cv2
import numpy as np

def psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    return 20 * np.log10(PIXEL_MAX / np.sqrt(mse))

# 读取图片
img1 = cv2.imread(r'C:\Users\win\Desktop\picture\2o.png')
img2 = cv2.imread(r'C:\Users\win\Desktop\picture\2a.png')

# 将图像转换为灰度图像
img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# 计算PSNR值
psnr_value = psnr(img1_gray, img2_gray)
print("PSNR value between image1 and image2 is:", psnr_value)