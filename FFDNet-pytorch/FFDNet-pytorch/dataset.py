"""
数据集相关函数
"""
import os
import os.path
import random
import glob
import numpy as np
import cv2
import h5py
import torch
import torch.utils.data as udata
from utils import data_augmentation, normalize

def img_to_patches(img, win, stride=1):
	"""
	将图像（image）转化为块阵列(array of patches)
	patch 可以通俗地理解为图像块，当需要处理的图像分辨率太大而资源受限(比如显存、算力等)时，就可以将图像划分成一个个小块
	这些小的图像块就是 patch，划分 patch 只是把原来的大图分成一个个小图，而这些小图依然是原图的部分，像素值没有改动
	因而在理论上，训练出来模型的上限能够比基于resize得到的图像训练来的高。
	在神经网络中，图像被表示成[c, h, w]格式或者[n, c, h, w]格式
		n：样本数量
		c：图像通道数
		w：图像宽度
		h：图像高度
	参数:
	img: 1个 numpy 阵列，包含了 CxHxW RGB (C=3，三通道) 或者 灰度值 (C=1，单通道)
	win: 输出的 块 的尺寸
	stride: int. stride 每次移动的步长
	"""
	k = 0
	endc = img.shape[0]
	endw = img.shape[1]
	endh = img.shape[2]
	patch = img[:, 0:endw-win+0+1:stride, 0:endh-win+0+1:stride]
	total_pat_num = patch.shape[1] * patch.shape[2]
	res = np.zeros([endc, win*win, total_pat_num], np.float32)
	for i in range(win):
		for j in range(win):
			patch = img[:, i:endw-win+i+1:stride, j:endh-win+j+1:stride]
			res[:, k, :] = np.array(patch[:]).reshape(endc, total_pat_num)
			k = k + 1
	return res.reshape([endc, win, win, total_pat_num])

def prepare_data(data_path, val_data_path, patch_size, stride, max_num_patches=None, aug_times=1, gray_mode=False):
	"""
	通过扫描相应的图像目录，并从中提取 块 来构建训练和验证数据集

	参数:
		data_path: 包含训练图像数据集的路径
		val_data_path: 包含验证图像数据集的路径
		patch_size: 从图像中提取的 图像块 的尺寸
		stride: 提取 图像块 的步幅大小
		max_num_patches: 要提取的 图像块 的最大数量
		aug_times: 增加可用数据的次数减 1
		gray_mode: 构建由灰度 图像块 组成的数据库
	"""
	# 训练数据库
	print('> Training database')
	scales = [1, 0.9, 0.8, 0.7]
	types = ('*.bmp', '*.png')
	files = []
	for tp in types:
		files.extend(glob.glob(os.path.join(data_path, tp)))
	files.sort()

	if gray_mode:
		traindbf = 'train_gray.h5'
		valdbf = 'val_gray.h5'
	else:
		traindbf = 'train_rgb.h5'
		valdbf = 'val_rgb.h5'

	if max_num_patches is None:
		max_num_patches = 5000000
		print("\tMaximum number of patches not set")
	else:
		print("\tMaximum number of patches set to {}".format(max_num_patches))

	train_num = 0
	i = 0
	with h5py.File(traindbf, 'w') as h5f:
		while i < len(files) and train_num < max_num_patches:
			imgor = cv2.imread(files[i])
			# h, w, c = img.shape
			for sca in scales:
				img = cv2.resize(imgor, (0, 0), fx=sca, fy=sca, interpolation=cv2.INTER_CUBIC)
				if not gray_mode:
					# CxHxW RGB image
					img = (cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).transpose(2, 0, 1)
				else:
					# CxHxW grayscale image (C=1)
					img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
					img = np.expand_dims(img, 0)

				img = normalize(img)
				patches = img_to_patches(img, win=patch_size, stride=stride)
				print("\tfile: %s scale %.1f # samples: %d" % \
					  (files[i], sca, patches.shape[3]*aug_times))
				for nx in range(patches.shape[3]):
					data = data_augmentation(patches[:, :, :, nx].copy(), np.random.randint(0, 7))
					h5f.create_dataset(str(train_num), data=data)
					train_num += 1
					for mx in range(aug_times-1):
						data_aug = data_augmentation(data, np.random.randint(1, 4))
						h5f.create_dataset(str(train_num)+"_aug_%d" % (mx+1), data=data_aug)
						train_num += 1
			i += 1

	# 验证数据库
	print('\n> Validation database')
	files = []
	for tp in types:
		files.extend(glob.glob(os.path.join(val_data_path, tp)))
	files.sort()
	h5f = h5py.File(valdbf, 'w')
	val_num = 0
	for i, item in enumerate(files):
		print("\tfile: %s" % item)
		img = cv2.imread(item)
		if not gray_mode:
			# C. H. W, RGB image 彩色图
			img = (cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).transpose(2, 0, 1)
		else:
			# C, H, W grayscale image (C=1) 灰度图
			img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			img = np.expand_dims(img, 0)
		img = normalize(img)
		h5f.create_dataset(str(val_num), data=img)
		val_num += 1
	h5f.close()

	print('\n> Total')
	print('\ttraining set, # samples %d' % train_num)
	print('\tvalidation set, # samples %d\n' % val_num)

class Dataset(udata.Dataset):
	"""
	执行 torch.utils.data.Dataset
	"""
	def __init__(self, train=True, gray_mode=False, shuffle=False):
		super(Dataset, self).__init__()
		self.train = train
		self.gray_mode = gray_mode
		if not self.gray_mode:
			self.traindbf = 'train_rgb.h5'
			self.valdbf = 'val_rgb.h5'
		else:
			self.traindbf = 'train_gray.h5'
			self.valdbf = 'val_gray.h5'

		if self.train:
			h5f = h5py.File(self.traindbf, 'r')
		else:
			h5f = h5py.File(self.valdbf, 'r')
		self.keys = list(h5f.keys())
		if shuffle:
			random.shuffle(self.keys)
		h5f.close()

	def __len__(self):
		return len(self.keys)

	def __getitem__(self, index):
		if self.train:
			h5f = h5py.File(self.traindbf, 'r')
		else:
			h5f = h5py.File(self.valdbf, 'r')
		key = self.keys[index]
		data = np.array(h5f[key])
		h5f.close()
		return torch.Tensor(data)
