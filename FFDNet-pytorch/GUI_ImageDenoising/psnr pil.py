import os
import numpy as np
from PIL import Image


def batch_psnr(dir1, dir2):

    assert os.path.exists(dir1), f"Invalid directory: {dir1}"
    assert os.path.exists(dir2), f"Invalid directory: {dir2}"

#获取两个目录中的图像文件列表，并对列表进行排序。
    img_list1 = sorted(os.listdir(dir1))
    img_list2 = sorted(os.listdir(dir2))
    assert len(img_list1) == len(img_list2), "The number of images in two directories is not equal"
#创建一个空列表 psnrs，用于存储每对图像的PSNR值。
    psnrs = []
    #使用 zip() 函数迭代遍历 img_list1 和 img_list2 中的图像文件名，
    # 每次迭代得到一对图像文件名 img1_name 和 img2_name。
    for img1_name, img2_name in zip(img_list1, img_list2):
        #根据目录 dir1 和图像文件名 img1_name 构建图像1的完整路径。
        img1_path = os.path.join(dir1, img1_name)
        img2_path = os.path.join(dir2, img2_name)
        #使用PIL库的 Image.open() 函数打开图像1，并将其转换为RGB模式。
        img1 = Image.open(img1_path).convert('RGB')
        img2 = Image.open(img2_path).convert('RGB')

        #如果图像1和图像2的尺寸不同，使用PIL库的 resize() 函数将图像2调整为与图像1相同的尺寸。
        if img1.size != img2.size:
            img2 = img2.resize(img1.size, resample=Image.BILINEAR)

        # calculate PSNR
        #首先，将图像1和图像2转换为NumPy数组，然后计算它们之间每个像素值的差的平方，最后求取平均值。
        mse = np.mean((np.array(img1) - np.array(img2)) ** 2)
        psnr = 10 * np.log10(255 ** 2 / mse)
        #将计算得到的PSNR值添加到列表 psnrs 中。
        psnrs.append(psnr)
        print(f"PSNR of {img1_name} and {img2_name}: {psnr:.2f}")

    avg_psnr = sum(psnrs) / len(psnrs)
    print(f"Average PSNR: {avg_psnr:.2f}")


if __name__ == '__main__':
    dir1 = r"C:\Users\win\Desktop\picture\test\Set12"
    dir2 = r"C:\Users\win\Desktop\picture\test\set12dncnn sa"
    batch_psnr(dir1, dir2)
