clc;clear all
% 选择任一图片
data_path = 'D:\pythonProject\UnfinishedBuilding\dataset\';
full_path = [data_path,'8068.mat'];
load(full_path)
% load('100007.mat')
% load('103006.mat')
% load('80090.mat')
% load('3063.mat')

%% 模拟训练
data0 = (groundTruth{1, 1}.Boundaries == 0);  % 对于MATLAB中的二值图像，0为黑，1为白
[x y] = find(groundTruth{1, 1}.Boundaries);   % 找出边缘坐标
% 可以修改loss和epoch参数来获得想要的效果
loss = 50;                                    % 类比混乱程度
epoch = 2;                                    % 类比训练次数，实际是过程的图片张数
Data0 = ones(size(data0));                    % 初始化模仿图像
for N = 1:epoch
    X = ceil(abs(x + loss*rand(size(x)) - loss/2));
    Y = ceil(abs(y + loss*rand(size(y)) - loss/2));
    for n = 1:length(X)
        Data0(X(n),Y(n)) = 0;
    end
    loss = loss - 24;
    figure(),imshow(Data0==0)
end
figure(),imshow(Data0==0 | data0==0)
