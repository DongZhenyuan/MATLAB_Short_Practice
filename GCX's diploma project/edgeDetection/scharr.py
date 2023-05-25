import cv2

def scharr(img):
  x = cv2.Scharr(img, cv2.CV_16S, 1, 0) # X 方向
  y = cv2.Scharr(img, cv2.CV_16S, 0, 1) # Y 方向
  absX = cv2.convertScaleAbs(x)
  absY = cv2.convertScaleAbs(y)
  return cv2.addWeighted(absX, 0.5, absY, 0.5, 0)