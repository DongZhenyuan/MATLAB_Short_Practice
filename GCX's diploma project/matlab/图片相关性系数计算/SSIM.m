function ssim_value = SSIM(original_image, processed_image)
    % ����ƫ������Ȩ�غͳ���
    k1 = 0.01;
    k2 = 0.03;
    L = 255;

    % ������ͼ��ת��Ϊ˫����
    original_image = im2double(original_image);
    processed_image = im2double(processed_image);

    % �����ֵ�������Э����
    mu_x = mean2(original_image);
    mu_y = mean2(processed_image);
    sigma_x = std2(original_image);
    sigma_y = std2(processed_image);
    cov_xy = cov(original_image(:), processed_image(:));

    % ����ṹ������ָ��
    ssim_value = ((2 * mu_x * mu_y + k1) * (2 * cov_xy(1, 2) + k2)) / ...
        ((mu_x^2 + mu_y^2 + k1) * (sigma_x^2 + sigma_y^2 + k2));
end