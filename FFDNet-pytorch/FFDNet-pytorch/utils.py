"""
这里提供了不同的实用程序，如权值的正交化、记录器的初始化等
"""
import subprocess
import math
import logging
import numpy as np
import cv2
import torch
import torch.nn as nn
from skimage.measure.simple_metrics import compare_psnr
from skimage.metrics import peak_signal_noise_ratio
'''
库更新警告(已消除):
UserWarning: DEPRECATED: skimage.measure.compare_psnr has been moved to skimage.metrics.peak_signal_noise_ratio.
It will be removed from skimage.measure in version 0.18.
因为skimage库的更新，compare_psnr 函数的位置将在未来发生变动，这里使用新的函数: peak_signal_noise_ratio
'''


def weights_init_kaiming(lyr):
	"""
	根据 "He" 初始化方法，对模型的权重进行初始化
	该方法在论文
	"Delving deep into rectifiers: Surpassing human-level performance on ImageNet classification" - He, K. et al. (2015)
	中使用正态分布
	此函数将被 torch.nn.Module.apply() 方法调用，该方法将 weights_init_kaiming() 应用于模型的每一层。
	"""
	classname = lyr.__class__.__name__
	if classname.find('Conv') != -1:
		nn.init.kaiming_normal(lyr.weight.data, a=0, mode='fan_in')
	elif classname.find('Linear') != -1:
		nn.init.kaiming_normal(lyr.weight.data, a=0, mode='fan_in')
	elif classname.find('BatchNorm') != -1:
		lyr.weight.data.normal_(mean=0, std=math.sqrt(2./9./64.)).\
			clamp_(-0.025, 0.025)
		nn.init.constant(lyr.bias.data, 0.0)

def batch_psnr(img, imclean, data_range):
	r"""
	按照 batch 为维度计算 PSNR (并非像素级别)

	Args:
		img: a `torch.Tensor` 包含恢复图像放大
		imclean: a `torch.Tensor` 包含参考图像
		data_range: 输入图片的数据范围 (最小值和最大值的可能的距离)。默认情况下，这是根据图像数据类型估计的。
	"""
	img_cpu = img.data.cpu().numpy().astype(np.float32)
	imgclean = imclean.data.cpu().numpy().astype(np.float32)
	psnr = 0
	for i in range(img_cpu.shape[0]):
		# psnr += compare_psnr(imgclean[i, :, :, :], img_cpu[i, :, :, :], data_range=data_range)
		psnr += peak_signal_noise_ratio(imgclean[i, :, :, :], img_cpu[i, :, :, :], data_range=data_range)
	return psnr/img_cpu.shape[0]

def data_augmentation(image, mode):
	"""
	对输入图像执行数据增强
	Args:
		image: a cv2 (OpenCV) image
		mode: int. Choice of transformation to apply to the image
			0 - 无变化
			1 - 上下翻转
			2 - 旋转 counterwise 90°
			3 - 旋转 90° 并上下翻转
			4 - 旋转 180°
			5 - 旋转 180° 并翻转
			6 - 旋转 270°
			7 - 旋转 270° 并翻转
	"""
	out = np.transpose(image, (1, 2, 0))
	if mode == 0:
		# original
		out = out
	elif mode == 1:
		# 上下翻转
		out = np.flipud(out)
	elif mode == 2:
		# 旋转 counterwise 90°
		out = np.rot90(out)
	elif mode == 3:
		# 旋转 90° 并上下翻转
		out = np.rot90(out)
		out = np.flipud(out)
	elif mode == 4:
		# 旋转 180°
		out = np.rot90(out, k=2)
	elif mode == 5:
		# 旋转 180° 并翻转
		out = np.rot90(out, k=2)
		out = np.flipud(out)
	elif mode == 6:
		# 旋转 270°
		out = np.rot90(out, k=3)
	elif mode == 7:
		# 旋转 270° 并翻转
		out = np.rot90(out, k=3)
		out = np.flipud(out)
	else:
		raise Exception('Invalid choice of image transformation')  # 出现其它数字则返回”无效的图像变换选择“
	return np.transpose(out, (2, 0, 1))

def variable_to_cv2_image(varim):
	"""
	将 torch.autograd.Variable 转换为 OpenCV 图像
	Args:
		varim: a torch.autograd.Variable
	"""
	nchannels = varim.size()[1]
	if nchannels == 1:
		res = (varim.data.cpu().numpy()[0, 0, :]*255.).clip(0, 255).astype(np.uint8)
	elif nchannels == 3:
		res = varim.data.cpu().numpy()[0]
		res = cv2.cvtColor(res.transpose(1, 2, 0), cv2.COLOR_RGB2BGR)
		res = (res*255.).clip(0, 255).astype(np.uint8)
	else:
		raise Exception('Number of color channels not supported')
	return res

def get_git_revision_short_hash():
	"""
	返回当前Git提交
	"""
	return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip()

def init_logger(argdict):
	"""
	初始化日志，将所有运行时参数保存到日志文件中
	Args:
		argdict: 要记录的参数字典
	"""
	from os.path import join

	logger = logging.getLogger(__name__)
	logger.setLevel(level=logging.INFO)
	fh = logging.FileHandler(join(argdict.log_dir, 'log.txt'), mode='a')
	formatter = logging.Formatter('%(asctime)s - %(message)s')
	fh.setFormatter(formatter)
	logger.addHandler(fh)
	try:
		logger.info("Commit: {}".format(get_git_revision_short_hash()))
	except Exception as e:
		logger.error("Couldn't get commit number: {}".format(e))
	logger.info("Arguments: ")
	for k in argdict.__dict__:
		logger.info("\t{}: {}".format(k, argdict.__dict__[k]))

	return logger

def init_logger_ipol():
	"""
	初始化日志。记录器 logger 用于在测试模型后记录结果

	Args:
		result_dir: 去噪结果文件夹的路径
	"""
	logger = logging.getLogger('testlog')
	logger.setLevel(level=logging.INFO)
	fh = logging.FileHandler('out.txt', mode='w')
	formatter = logging.Formatter('%(message)s')
	fh.setFormatter(formatter)
	logger.addHandler(fh)

	return logger

def init_logger_test(result_dir):
	"""
	初始化日志。记录器 logger 用于在测试模型后记录结果

	Args:
		result_dir: 去噪结果文件夹的路径
	"""
	from os.path import join

	logger = logging.getLogger('testlog')
	logger.setLevel(level=logging.INFO)
	fh = logging.FileHandler(join(result_dir, 'log.txt'), mode='a')
	formatter = logging.Formatter('%(asctime)s - %(message)s')
	fh.setFormatter(formatter)
	logger.addHandler(fh)

	return logger

def normalize(data):
	"""
	在 [0,1] 范围内的 unit8 图像归一化为 float32 图像

	Args:
		data: 将 [0, 255] 的 unint8 numpy数组标准化化为 [0, 1]
	"""
	return np.float32(data/255.)

def svd_orthogonalization(lyr):
	"""
	通过执行论文
	"FFDNet: Toward a fast and flexible solution for CNN based image denoising." Zhang et al. (2017)
	中描述的正交化方法，来将正则化应用于训练
	对于模型中的每个卷积层，该方法用相互正交的新滤波器来代替以层滤波器为列的矩阵。
	这可以通过将 SVD分解 的奇异值设置为 1 来实现。

	此函数将由 torch.nn.Module.apply() 方法调用，该方法将 svd_orthogonalization() 应用于模型的每一层。
	"""
	classname = lyr.__class__.__name__
	if classname.find('Conv') != -1:
		weights = lyr.weight.data.clone()
		c_out, c_in, f1, f2 = weights.size()
		dtype = lyr.weight.data.type()

		# Reshape filters to columns
		# From (c_out, c_in, f1, f2)  to (f1*f2*c_in, c_out)
		weights = weights.permute(2, 3, 1, 0).contiguous().view(f1*f2*c_in, c_out)

		# Convert filter matrix to numpy array
		weights = weights.cpu().numpy()

		# SVD decomposition and orthogonalization
		mat_u, _, mat_vh = np.linalg.svd(weights, full_matrices=False)
		weights = np.dot(mat_u, mat_vh)

		# As full_matrices=False we don't need to set s[:] = 1 and do mat_u*s
		lyr.weight.data = torch.Tensor(weights).view(f1, f2, c_in, c_out).\
			permute(3, 2, 0, 1).type(dtype)
	else:
		pass

def remove_dataparallel_wrapper(state_dict):
	"""
	通过移除模块字典中的 module封装器，将数据并行模型转换为普通模型

	Args:
		state_dict: a torch.nn.DataParallel state dictionary
	"""
	from collections import OrderedDict

	new_state_dict = OrderedDict()
	for k, vl in state_dict.items():
		name = k[7:]     # remove 'module.' of DataParallel
		new_state_dict[name] = vl

	return new_state_dict

def is_rgb(im_path):
	"""
	如果 im_path 路径下的图片为彩色图，则返回 True
	"""
	from skimage.io import imread
	rgb = False
	im = imread(im_path)
	if (len(im.shape) == 3):
		if not(np.allclose(im[...,0], im[...,1]) and np.allclose(im[...,2], im[...,1])):
			rgb = True
	print("rgb: {}".format(rgb))
	print("im shape: {}".format(im.shape))
	return rgb
