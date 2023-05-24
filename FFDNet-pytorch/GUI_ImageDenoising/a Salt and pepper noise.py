import os
import cv2
import numpy as np

def add_salt_and_pepper(img, noise_level):
    """
    在图像中添加椒盐噪声。

    Args:
    - img: numpy数组类型的图像，像素值在[0,255]之间。
    - noise_level: 噪声强度，取值在[0,1]之间，表示噪声点占总像素点数的比例。

    Returns:
    - noisy_img: 添加了椒盐噪声的图像。
    """
    noisy_img = img.copy()

    # 计算需要添加的噪声点个数
    num_noise_pixels = int(noise_level * img.shape[0] * img.shape[1])

    # 生成一个与原始图像大小相同的随机数矩阵
    noise_matrix = np.random.rand(img.shape[0], img.shape[1])

    # 将矩阵中小于0.5 - noise_level/2的元素设置为0，大于0.5 + noise_level/2的元素设置为1
    noise_matrix[noise_matrix < 0.5 - noise_level / 2] = 0
    noise_matrix[noise_matrix > 0.5 + noise_level / 2] = 1

    # 在原始图像中添加噪声点
    # 将随机选择的位置对应的像素点设置为0或255
    for i in range(num_noise_pixels):
        x = np.random.randint(img.shape[0])
        y = np.random.randint(img.shape[1])
        if noise_matrix[x, y] == 0:
            noisy_img[x, y] = 0
        else:
            noisy_img[x, y] = 255

    return noisy_img


# Set paths to input and output folders
input_folder_path = r"C:\Users\win\Desktop\picture\test\Set12"
output_folder_path = r"C:\Users\win\Desktop\picture\test\Set12 Sa"

# Set the density of salt and pepper noise to be added
density = 0.05

# Loop over all files in the input folder
for filename in os.listdir(input_folder_path):
    # Check if the file is an image file
    if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
        # Read the image file
        img_path = os.path.join(input_folder_path, filename)
        img = cv2.imread(img_path)
        # Add salt and pepper noise to the image
        noisy_image = add_salt_and_pepper(img, density)
        # Save the noisy image to the output folder
        output_path = os.path.join(output_folder_path, filename)
        cv2.imwrite(output_path, noisy_image)
