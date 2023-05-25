'''
简短到令人发指，openCV牛逼！
'''
import cv2

def LOG(img):
  # 先通过高斯滤波降噪
  gaussian = cv2.GaussianBlur(img, (3, 3), 0)
  # 再通过拉普拉斯算子做边缘检测
  dst = cv2.Laplacian(gaussian, cv2.CV_16S, ksize=3)
  return cv2.convertScaleAbs(dst)