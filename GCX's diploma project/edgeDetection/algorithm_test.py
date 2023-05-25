"""
各种边缘分割算子的测试框架
"""
import cv2
import numpy as np
from sobel import sobel
from canny import canny
from laplacian import laplacian



Original_img = cv2.imread(r"D:\pythonProject\UnfinishedBuilding\images\12003.jpg", 0)
Grayscale_img = cv2.imread(r"D:\pythonProject\UnfinishedBuilding\images\12003.jpg", cv2.IMREAD_GRAYSCALE)

finished_img1 = sobel(Grayscale_img)
finished_img2 = canny(Grayscale_img)
finished_img3 = laplacian(Grayscale_img)
# 对边缘检测后返回的图像进行二值化处理
_, binary1 = cv2.threshold(finished_img1, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
_, binary2 = cv2.threshold(finished_img2, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
_, binary3 = cv2.threshold(finished_img3, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

binary = binary1 * binary2 * binary3

print(binary)

cv2.imshow('Image', binary)

cv2.waitKey(0)
cv2.destroyAllWindows()

