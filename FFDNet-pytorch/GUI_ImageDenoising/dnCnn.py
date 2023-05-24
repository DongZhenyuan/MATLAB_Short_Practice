import cv2
import os
import argparse
import glob
import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable

from DnCNN.models import DnCNN
from DnCNN.utils import *


os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # 按照PCI_BUS_ID顺序从0开始排列GPU设备
os.environ["CUDA_VISIBLE_DEVICES"] = "0"         # 设置当前使用的GPU设备仅为0号设备  设备名称为'/gpu:0'
# 参数配置
parser = argparse.ArgumentParser(description="DnCNN_Test")                                            # 指定模型名称
parser.add_argument("--num_of_layers", type=int, default=17, help="Number of total layers")           # 指定模型的层数为17
parser.add_argument("--logdir", type=str, default="DnCNN/logs/DnCNN-S-50", help='path of log files')  # 指定模型日志的名称和路径
parser.add_argument("--test_data", type=str, default='Set12', help='test on Set12 or Set68')          # 指定测试集名称
parser.add_argument("--test_noiseL", type=float, default=25, help='noise level used on test set')     # 指定加在测试集行的噪声
opt = parser.parse_args()                                                                             # 将所有配置返回给变量opt


def normalize(data):
    """
    图形数据归一化
    """
    return data/255.


def dncnn_eval(pic_path, output_path):
    """
    构建模型
    """
    print('Loading model ...\n')
    net = DnCNN(channels=1, num_of_layers=opt.num_of_layers)
    device_ids = [0]
    model = nn.DataParallel(net, device_ids=device_ids).cuda()
    model.load_state_dict(torch.load(os.path.join(opt.logdir, 'net.pth')))
    model.eval()

    # 加载数据信息
    print('Loading data info ...\n')
    files_source = glob.glob(os.path.join('DnCNN/data', opt.test_data, '*.png'))
    files_source.sort()

    # 进程数据
    psnr_test = 0

    # 图像
    Img = cv2.imread(pic_path)
    Img = normalize(np.float32(Img[:, :, 0]))
    Img = np.expand_dims(Img, 0)
    Img = np.expand_dims(Img, 1)
    ISource = torch.Tensor(Img)

    # 噪声
    noise = torch.FloatTensor(ISource.size()).normal_(mean=0, std=opt.test_noiseL/255.)

    # 图像加噪
    INoisy = ISource + noise
    ISource, INoisy = Variable(ISource.cuda()), Variable(INoisy.cuda())
    # 这可以节约大量内存
    with torch.no_grad():
        Out = torch.clamp(INoisy-model(INoisy), 0., 1.)
    save_out = np.uint8(255 * Out.detach().cpu().numpy().squeeze())  # back to cpu
    cv2.imwrite(output_path,save_out)


    # cv2.imshow('',save_out)

    ## if you are using older version of PyTorch, torch.no_grad() may not be supported
    # ISource, INoisy = Variable(ISource.cuda(),volatile=True), Variable(INoisy.cuda(),volatile=True)
    # Out = torch.clamp(INoisy-model(INoisy), 0., 1.)
    psnr = batch_PSNR(Out, ISource, 1.)
    psnr_test += psnr
