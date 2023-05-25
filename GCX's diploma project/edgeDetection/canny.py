"""
cv2.Canny(image,            # 输入原图（必须为单通道图）
          threshold1, 
          threshold2,       # 较大的阈值2用于检测图像中明显的边缘
          [, edges[, 
          apertureSize[,    # apertureSize：Sobel算子的大小
          L2gradient ]]])   # 参数(布尔值)：
                              true： 使用更精确的L2范数进行计算（即两个方向的倒数的平方和再开放），
                              false：使用L1范数（直接将两个方向导数的绝对值相加）。
"""
import cv2

def canny(img):
    """"canny(): 边缘检测"""
    img = cv2.GaussianBlur(img, (3, 3), 0)
    canny = cv2.Canny(img, 50,150)
    return canny

def morphology(img):
    """形态学：边缘检测"""
    # 设定红色通道阈值210（阈值影响梯度运算效果）
    _, Thr_img = cv2.threshold(img, 210, 255, cv2.THRESH_BINARY)
    # 定义矩形结构元素
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    # 梯度
    gradient = cv2.morphologyEx(Thr_img, cv2.MORPH_GRADIENT, kernel)
    return gradient
