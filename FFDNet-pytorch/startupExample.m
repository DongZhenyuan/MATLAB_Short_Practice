% 本脚本将配置 MATLAB 搜索路径，使目标文件夹中的所有脚本、函数等都彼此可见
%% 启动脚本
% Matconvnet安装教程较为繁杂，我的处理是将Matconvnet解压后和项目放在一个目录中
% 使用addpath(genpath('相对路径'))直接添加到MATLAB路径中，虽然会返回警告，但亲测有效
clear, clc, close all;
disp('Starting Projects...')
addpath(genpath('matconvnet-1.0-beta25\matconvnet-1.0-beta25'))
addpath(genpath('matconvnet-1.0-beta25\matconvnet-1.0-beta25\matlab'))
addpath(genpath('matconvnet-1.0-beta25\matconvnet-1.0-beta25\matlab\simplenn'))
% 因为文件 matconvnet-1.0-beta25 中存在一些与内置函数同名的函数，所以会返回警告，这里选择无视
clc
disp('Ready to Go')