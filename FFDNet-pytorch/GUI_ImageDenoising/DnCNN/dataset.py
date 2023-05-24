"""
本文件参考代码来自：http://www.ipol.im/pub/art/2019/231/
"""
import os
import os.path
import random
import glob
import numpy as np
import cv2
# import h5py
import torch
import torch.utils.data as udata
from utils import data_augmentation

def normalize(data):
    return data/255.

def img_to_patches(img, win, stride=1):
    """
    将图像（image）转化为碎片阵列(array of patches)
    patch可以通俗地理解为图像块
    当需要处理的图像分辨率太大而资源受限(比如显存、算力等)时，就可以将图像划分成一个个小块，这些小的图像块就是patch
    划分patch只是把原来的大图分成一个个小图，而这些小图依然是原图的部分，像素值没有改动
    因而在理论上，训练出来模型的上限能够比基于resize得到的图像训练来的高。
    参数:
    img: 1个 numpy 阵列，包含了 CxHxW RGB (C=3，三通道) or 灰度值 (C=1，单通道)
        image
        在神经网络中，图像被表示成[c, h, w]格式或者[n, c, h, w]格式
        n：样本数量
        c：图像通道数
        w：图像宽度
        h：图像高度
    win: 输出 patches 的尺寸
    stride: int. stride 每次移动的步长
    """
    k = 0
    endc = img.shape[0]    # 通道数
    endw = img.shape[1]    # 图像宽度
    endh = img.shape[2]    # 图像高度
    patch = img[:, 0:endw-win+0+1:stride, 0:endh-win+0+1:stride]
    total_pat_num = patch.shape[1] * patch.shape[2]
    res = np.zeros([endc, win*win, total_pat_num], np.float32)
    for i in range(win):
        for j in range(win):
            patch = img[:, i:endw-win+i+1:stride, j:endh-win+j+1:stride]
            res[:, k, :] = np.array(patch[:]).reshape(endc, total_pat_num)
            k = k + 1
    return res.reshape([endc, win, win, total_pat_num])

def prepare_data(data_path, patch_size, stride, aug_times=1):
    # train
    print('process training data')
    scales = [1, 0.9, 0.8, 0.7]
    files = glob.glob(os.path.join(data_path, 'train', '*.png'))
    files.sort()
    h5f = h5py.File('train.h5', 'w')
    train_num = 0
    for i in range(len(files)):
        img = cv2.imread(files[i])
        h, w, c = img.shape
        for k in range(len(scales)):
            Img = cv2.resize(img, (int(h*scales[k]), int(w*scales[k])), interpolation=cv2.INTER_CUBIC)
            Img = np.expand_dims(Img[:,:,0].copy(), 0)
            Img = np.float32(normalize(Img))
            patches = img_to_patches(Img, win=patch_size, stride=stride)
            print("file: %s scale %.1f # samples: %d" % (files[i], scales[k], patches.shape[3]*aug_times))
            for n in range(patches.shape[3]):
                data = patches[:,:,:,n].copy()
                h5f.create_dataset(str(train_num), data=data)
                train_num += 1
                for m in range(aug_times-1):
                    data_aug = data_augmentation(data, np.random.randint(1,8))
                    h5f.create_dataset(str(train_num)+"_aug_%d" % (m+1), data=data_aug)
                    train_num += 1
    h5f.close()
    # val
    print('\nprocess validation data')
    files.clear()
    files = glob.glob(os.path.join(data_path, 'Set12', '*.png'))
    files.sort()
    h5f = h5py.File('val.h5', 'w')
    val_num = 0
    for i in range(len(files)):
        print("file: %s" % files[i])
        img = cv2.imread(files[i])
        img = np.expand_dims(img[:, :, 0], 0)  # 处理的是单通道的灰度图
        img = np.float32(normalize(img))
        h5f.create_dataset(str(val_num), data=img)
        val_num += 1
    h5f.close()

    print('\n> Total')
    print('\ttraining set, # samples %d\n' % train_num)
    print('\tval set, # samples %d\n' % val_num)

class Dataset(udata.Dataset):
    """
    使 torch.utils.data.Dataset 生效
    """
    # def __init__(self, train=True, gray_mode=False, shuffle=False):
    def __init__(self, train=True):
        super(Dataset, self).__init__()
        self.train = train
        """
        self.gray_mode = gray_mode
        if not self.gray_mode:
            self.traindbf = 'train_rgb.h5'
            self.valdbf = 'val_rgb.h5'
        else:
            self.traindbf = 'train_gray.h5'
            self.valdbf = 'val_gray.h5'
        """
        if self.train:
            h5f = h5py.File('train.h5', 'r')
        else:
            h5f = h5py.File('val.h5', 'r')
        self.keys = list(h5f.keys())
        """
        这是原文件的写法
        if shuffle:
            random.shuffle(self.keys)
        h5f.close()
        """
        random.shuffle(self.keys)
        h5f.close()

    def __len__(self):
        return len(self.keys)

    def __getitem__(self, index):
        if self.train:
            h5f = h5py.File('train.h5', 'r')    # 没找到train.h5这个文件
        else:
            h5f = h5py.File('val.h5', 'r')      # val.h5倒是有
        key = self.keys[index]
        data = np.array(h5f[key])
        h5f.close()
        return torch.Tensor(data)
