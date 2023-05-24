"""
实现自定义NN层的函数
"""
import torch
from torch.autograd import Function, Variable

def concatenate_input_noise_map(input, noise_sigma):
	"""
	实现FFDNet的第一层
	这个函数返回一个 torch.autograd.Variable，该变量由下采样的输入图像和噪声映射的连接组成
	一批大小为 CxHxW 的每个图像被转换为大小为 4*CxH/2xW/2 的数组
	输入图像的非重叠 2x2 块的每个像素都沿着第一个维度放置在新的数组中

	Args:
		input: 包含一批 CxHxW 的图像
		noise_sigma: CxH/2xW/2 噪声映射的像素数值
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
	"""
	通过实现 torch.autograd.Function 来拓展 PyTorch 库的模块
	这个类实现了 FFDNet 最后一层的前向和后向方法
	它基本上是 concatenate_input_noise_map() 的逆过程
	将一批大小为 C x H/2 x W/2 的图像转换为大小为 C/4 x H x W 的图像
	"""
	@staticmethod
	def forward(ctx, input):
		N, Cin, Hin, Win = input.size()
		dtype = input.type()
		sca = 2
		sca2 = sca*sca
		Cout = Cin//sca2
		Hout = Hin*sca
		Wout = Win*sca
		idxL = [[0, 0], [0, 1], [1, 0], [1, 1]]

		assert (Cin%sca2 == 0), \
			'Invalid input dimensions: number of channels should be divisible by 4'

		result = torch.zeros((N, Cout, Hout, Wout)).type(dtype)
		for idx in range(sca2):
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
