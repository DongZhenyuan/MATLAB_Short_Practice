import os
import numpy as np
from PIL import Image

# 定义高斯噪声函数
def add_gaussian_noise(image, mean=0, std=0.1):
    """
    在图像上添加高斯噪声
    :param image: PIL.Image格式的图像
    :param mean: 噪声均值
    :param std: 噪声标准差
    :return: 添加噪声后的图像
    """
    img = np.array(image)
    noise = np.random.normal(mean, std, img.shape)
    out = img + noise
    out = np.clip(out, 0, 255).astype(np.uint8)
    out = Image.fromarray(out)
    return out

# 设置文件夹路径和保存路径
data_dir = r"C:\Users\win\Desktop\picture\Set12"
save_dir = r"C:\Users\win\Desktop\picture\Set12 Gn"

# 批量处理每张图片
for filename in os.listdir(data_dir):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        img_path = os.path.join(data_dir, filename)
        image = Image.open(img_path)
        # 给图像添加高斯噪声
        noisy_image = add_gaussian_noise(image, mean=0, std=10)
        # 保存处理后的图像
        save_path = os.path.join(save_dir, filename)
        noisy_image.save(save_path)
