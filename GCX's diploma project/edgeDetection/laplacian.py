'''
简短到令人发指，openCV牛逼！
'''
import cv2

def laplacian(img):
  dst = cv2.Laplacian(img, cv2.CV_16S, ksize = 3)
  return cv2.convertScaleAbs(dst)