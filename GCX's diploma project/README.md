# 强化学习一言难尽
创建时间：2023/4/13周四  
结束时间：2023/4/27周四

本项目是为 GCX 创建的项目，其中杂糅了各种脚本，唯独没有基于 DQN(Deep Q-Network) 的图像边缘检测，简直是一片废墟……

---
## 主要文件

`DQN_Maze`文件夹：
DQN 算法的一个*demo*，用于路径规划。之后又做了一些修改，让迷宫中的奖励点呈现出图形的轮廓。

初始代码来自：https://github.com/ClownW/Reinforcement-learning-with-PyTorch/tree/master/content/5_Deep_Q_Network

`edgeDetection`文件夹：
使用传统图像分割算法进行边缘检测，这里用 *Tkinter* 工具包进行图形用户界面界面的开发。

`images`文件夹：作为图像边缘检测的素材库

`emoticons`文件夹：开发者的精神状态

`matlab`文件夹：一些 MATLAB 脚本，用于模拟 AI 行为、绘制评估线图、图像相关性系数计算

`BSR.zip`文件：由 GCX 提供，其中包括了图像边缘的二值矩阵(根据这些数据，编写 `DQN_Maze` 中的的奖励点分布和 `matlab` 文件中的AI 行为模拟)

---
### `matlab`文件说明

#### *评估线图绘制* 文件夹
Excel表格中的数据是用户自制的，只是为了能够画出像那么回事的图形
* `dataVisualization.m`：读入数据并绘制图形
* `myData.xlsx`：自制数据
* `photo.png`：将绘制的图形保存为便携式网络图形

&nbsp;

#### *图片相关性系数计算* 文件夹
这是为另外一名用户编写的脚本，用于逐帧计算图像之间的相关性系数，组成序列后绘制

* `视频消抖.zip`：从视频中逐帧抽取而来的图片，共120张
* `cov2D.xlsx`：计算相隔固定帧数的图片的二维相关系数
* `SSIM.m`：由用户提供，这里并未使用

&nbsp;

#### *dataset* 文件夹
这是为另外一名用户编写的脚本，用于逐帧计算图像之间的相关性系数，组成序列后绘制

* `mat_data`：图像边缘的二值矩阵，黑底白边
* `m_files`：包括  `pictureLocation.m` 脚本和 `fakeNet.m` 脚本，其中 `fakeNet.m` 脚本用于模拟 AI 行为
* `data`：保存 `pictureLocation.m` 脚本输出的边缘轮廓横纵坐标，作为 `DQN_Maze` 文件的输入数据
