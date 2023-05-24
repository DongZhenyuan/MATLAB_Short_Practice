"""
Functions implementing custom NN layers

Copyright (C) 2018, Matias Tassano <matias.tassano@parisdescartes.fr>

This program is free software: you can use, modify and/or
redistribute it under the terms of the GNU General Public
License as published by the Free Software Foundation, either
version 3 of the License, or (at your option) any later
version. You should have received a copy of this license along
this program. If not, see <http://www.gnu.org/licenses/>.
"""
import torch
from torch.autograd import Function, Variable

def concatenate_input_noise_map(input, noise_sigma):
	r"""Implements the first layer of FFDNet. This function returns a
	torch.autograd.Variable composed of the concatenation of the downsampled
	input image and the noise map. Each image of the batch of size CxHxW gets
	converted to an array of size 4*CxH/2xW/2. Each of the pixels of the
	non-overlapped 2x2 patches of the input image are placed in the new array
	along the first dimension.

	Args:
		input: batch containing CxHxW images
		noise_sigma: the value of the pixels of the CxH/2xW/2 noise map
	"""
	# noise_sigma is a list of length batch_size
	N, C, H, W = input.size()
	dtype = input.type()
	sca = 2
	sca2 = sca*sca
	Cout = sca2*C
	Hout = H//sca
	Wout = W//sca
	idxL = [[0, 0], [0, 1], [1, 0], [1, 1]]

	# Fill the downsampled image with zeros
	if 'cuda' in dtype:
		downsampledfeatures = torch.cuda.FloatTensor(N, Cout, Hout, Wout).fill_(0)
	else:
		downsampledfeatures = torch.FloatTensor(N, Cout, Hout, Wout).fill_(0)

	# Build the CxH/2xW/2 noise map
	noise_map = noise_sigma.view(N, 1, 1, 1).repeat(1, C, Hout, Wout)

	# Populate output
	for idx in range(sca2):
		downsampledfeatures[:, idx:Cout:sca2, :, :] = \
			input[:, :, idxL[idx][0]::sca, idxL[idx][1]::sca]

	# concatenate de-interleaved mosaic with noise map
	return torch.cat((noise_map, downsampledfeatures), 1)

class UpSampleFeaturesFunction(Function):
	# it converts each of the images of a batch of size CxH/2xW/2 to images of size C/4xHxW

	@staticmethod
	def forward(ctx, input):
		#N 表示批次大小（batch size），Cin 表示输入通道数（number of input channels）
		N, Cin, Hin, Win = input.size()
		dtype = input.type()
		#上采样放大因子
		sca = 2
		sca2 = sca*sca
		#通过将输入通道数除以放大因子的平方得到。//整数除法
		Cout = Cin//sca2
		Hout = Hin*sca
		Wout = Win*sca
		#上采样的索引位置
		idxL = [[0, 0], [0, 1], [1, 0], [1, 1]]
#能否整除
		assert (Cin%sca2 == 0), \
			'Invalid input dimensions: number of channels should be divisible by 4'
#创建一个全零张量 result，形状为 (N, Cout, Hout, Wout)，与输入张量具有相同的数据类型。
		result = torch.zeros((N, Cout, Hout, Wout)).type(dtype)
	#遍历 idx 从 0 到 sca2-1 的范围
		for idx in range(sca2):
#: 表示选择所有批次和通道的元素，idxL[idx][0]::sca 表示在高度维度上选择特定区域，
# idxL[idx][1]::sca 表示在宽度维度上选择特定区域。
			result[:, :, idxL[idx][0]::sca, idxL[idx][1]::sca] = \
				input[:, idx:Cin:sca2, :, :]

		return result

	@staticmethod
	def backward(ctx, grad_output):
		N, Cg_out, Hg_out, Wg_out = grad_output.size()
		dtype = grad_output.data.type()
		sca = 2
		sca2 = sca*sca
		Cg_in = sca2*Cg_out
		Hg_in = Hg_out//sca
		Wg_in = Wg_out//sca
		idxL = [[0, 0], [0, 1], [1, 0], [1, 1]]

		# Build output
		grad_input = torch.zeros((N, Cg_in, Hg_in, Wg_in)).type(dtype)
		# Populate output
		for idx in range(sca2):
			grad_input[:, idx:Cg_in:sca2, :, :] = \
				grad_output.data[:, :, idxL[idx][0]::sca, idxL[idx][1]::sca]

		return Variable(grad_input)

# Alias functions
upsamplefeatures = UpSampleFeaturesFunction.apply
