clc;
clear all
close  all

%% �õ�ͼƬ�����б�
fileName = '��Ƶ����';
img_structs = dir(fileName);
directory = natsortfiles(img_structs);
img_names = {directory.name};
img_names = img_names(3:end);

%% ȷ��ͼ����󳤿�
width = zeros(1,numel(img_names));
height = zeros(1,numel(img_names));
for idx = 1:numel(img_names)
    photo = imread([cd,'\',fileName,'\',img_names{idx}]);
    photo = rgb2gray(photo);
    width(idx) = size(photo,1);
    height(idx) = size(photo,2);
end

%% ���������ϵ������
r_seq = zeros(1,numel(img_names));
canvas1 = zeros(max(height),max(width));  % ��ʼ������
canvas2 = canvas1;
for idx = 1:(numel(img_names))-5
    current_photo = imread([cd,'\',fileName,'\',img_names{idx}]);
    current_photo = rgb2gray(current_photo);
    next_photo = imread([cd,'\',fileName,'\',img_names{idx+5}]);
    next_photo = rgb2gray(next_photo);
    % 8λ�޷���������תΪ˫����
    canvas1(1:size(current_photo,1),1:size(current_photo,2)) = double(current_photo);
    canvas2(1:size(next_photo,1),1:size(next_photo,2)) = double(next_photo);
    % ���ά�����ϵ��
    r_seq(idx) = corr2(canvas1,canvas2);
end
stem(r_seq,'.')
