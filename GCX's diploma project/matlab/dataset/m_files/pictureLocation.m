%% 飞机轮廓
load('3063.mat')
data0 = (groundTruth{1, 1}.Boundaries);
imshow(data0)
save(['C:\Users\dzy\Desktop\dataset\data\','data0'],'data0')
[x,y] = find(data0);
loc0 = [x,y];
save(['C:\Users\dzy\Desktop\dataset\data\','loc0'],'loc0')

%% 天鹅轮廓
clear all; clc
load('8068.mat')
data1 = (groundTruth{1, 1}.Boundaries);
imshow(data1)
save(['C:\Users\dzy\Desktop\dataset\data\','data1'],'data1')
[x,y] = find(data1);
loc1 = [x,y];
save(['C:\Users\dzy\Desktop\dataset\data\','loc1'],'loc1')

%% 北极熊轮廓
clear all; clc
load('100007.mat')
data2 = (groundTruth{1, 1}.Boundaries);
imshow(data2)
save(['C:\Users\dzy\Desktop\dataset\data\','data2'],'data2')
[x,y] = find(data2);
loc2 = [x,y];
save(['C:\Users\dzy\Desktop\dataset\data\','loc2'],'loc2')

%% 象龟轮廓
clear all; clc
load('103006.mat')
data3 = (groundTruth{1, 1}.Boundaries);
imshow(data3)
save(['C:\Users\dzy\Desktop\dataset\data\','data3'],'data3')
[x,y] = find(data3);
loc3 = [x,y];
save(['C:\Users\dzy\Desktop\dataset\data\','loc3'],'loc3')

%% 妇女背影
clear all; clc
load('80090.mat')
data4 = (groundTruth{1, 1}.Boundaries);
imshow(data4)
save(['C:\Users\dzy\Desktop\dataset\data\','data4'],'data4')
[x,y] = find(data4);
loc4 = [x,y];
save(['C:\Users\dzy\Desktop\dataset\data\','loc4'],'loc4')