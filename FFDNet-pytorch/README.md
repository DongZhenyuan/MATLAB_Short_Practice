# 概述
创建时间：2023/5/12周五  
结束时间：2023/5/18周四

原始项目来自客户，其中使用了 `PyQt` 工具包进行 GUI 应用程序的开发。其余关于模型构建和训练的代码均已找到出处

关于 DnCNN 的简易实现，来自：https://github.com/SaoYan/DnCNN-PyTorch

关于 FFDNet 图像去噪的 PyTorch 实现源码，来自：http://www.ipol.im/pub/art/2019/231/

以上是关于本项目的全部构成。

&nbsp;

关于网络性能的评估，可以参考：https://github.com/cszn/FFDNet

该评估项目的 MATLAB 纯度极高。
要运行代码，您应该先安装 Matconvnet。
或者使用函数 `vl_ffdnet_matlab` 在没有 Matconvnet 的情况下执行去噪。
在启动该项目之前，可以先安装 Matconvnet，再运行本目录中的 `startupExample.m` 以将 Matconvnet 放入 MATLAB 搜索路径

&nbsp;

以下是 *关于 FFDNet 图像去噪的 PyTorch 实现* 项目的描述
# 关于 FFDNet 图像去噪的 Pytorch 实现

* 作者：Matias Tassano <matias.tassano@parisdescartes.fr>
* 版权所有：(C) 2018 IPOL Image Processing On Line http://www.ipol.im/
* 许可证：GPL v3+，参见 GPLv3.txt

# 论文

as in Zhang, Kai, Wangmeng Zuo, and Lei Zhang.
"FFDNet: Toward a fast and flexible solution for CNN based image denoising."

arXiv 预印本

arXiv:1710.04026 (2017).

# 用户指南

此代码在 Python 3.6 中运行，具有以下依赖项：

## 依赖
* [PyTorch v0.3.1](http://pytorch.org/)
* [scikit-image](http://scikit-image.org/)
* [torchvision](https://github.com/pytorch/vision)
* [OpenCV](https://pypi.org/project/opencv-python/)
* [HDF5](http://www.h5py.org/)
* [tensorboardX](https://github.com/lanpa/tensorboard-pytorch)

## 用法

### 1. 测试

如果你想要使用其中一个预训练模型对图像进行降噪
在 *models* 文件目录中，你可以执行
```
python test_ffdnet_ipol.py \
	--input input.png \
	--noise_sigma 25 \
	--add_noise True
```
想要在 CPU 而非 GPU 上运行算法，请执行以下操作:
```
python test_ffdnet_ipol.py \
	--input input.png \
	--noise_sigma 25 \
	--add_noise True \
	--no_gpu
```
**备注**
* 模型已经针对 [0, 75] 中的噪声值进行了训练
* 如果输入图像已经有噪点，可以将 *add_noise* 设置为 *False*

### 2. 训练

#### 准备数据库

首先，您需要通过执行 *prepare_patches.py* 来准备由图像碎片组成的数据集，
通过分别传递 *--trainset_dir* 和 *--valset_dir* 来指明包含了训练集和验证集的目录的路径

本代码并没有提供图像数据集，在此提供下载地址：

* 训练集：[Waterloo Exploration Database](https://ece.uwaterloo.ca/~k29ma/exploration/)

* 验证集：[Kodak Lossless True Color Image Suite](http://r0k.us/graphics/kodak/)

**备注**
* 准备灰度数据集: ```python prepare_patches.py --gray```
* *--max_number_patches* 可用来设置包含在数据库内的最大图像碎片的数量

#### 训练模型

在建立了训练和验证数据库之后，可以对模型进行训练
(即 *train_rgb.h5* 和 *val_rgb.h5* 用作彩色图降噪, 而 *train_gray.h5* 和 *val_gray.h5* 用作灰度图降噪)。
仅支持在 GPU 上进行训练
```
python train.py \
	--batch_size 128 \
	--epochs 80 \
	--noiseIntL 0 75
	--val_noiseL 25
```
**备注**
* 训练进程将被 TensorBoard 监视，并作为日志保存至 *log_dir* 目录下
* 默认情况下，针对 [0, 75] 中的噪声值训练模型 (*--noiseIntL* 标志位)
* 默认情况下，验证时添加的噪声设置为 20 (*--val_noiseL* 标志位)
* 历史训练可通过置位 *--resume_training* 标志位进行恢复

# 关于此文件

版权所有 2018 IPOL 在线图像处理 http://www.ipol.im/

只要保留版权声明和本声明，无论是否修改，都允许在任何媒体上复制和分发本文件，而无需缴纳版税。
此文件按照原件提供，不作任何保障。

# 感谢

部分代码基于 Yiqi Yan 的代码<yanyiqinwpu@gmail.com>