function ssim_value = SSIM(original_image, processed_image)
    % 设置偏移量、权重和常数
    k1 = 0.01;
    k2 = 0.03;
    L = 255;

    % 将输入图像转换为双精度
    original_image = im2double(original_image);
    processed_image = im2double(processed_image);

    % 计算均值、方差和协方差
    mu_x = mean2(original_image);
    mu_y = mean2(processed_image);
    sigma_x = std2(original_image);
    sigma_y = std2(processed_image);
    cov_xy = cov(original_image(:), processed_image(:));

    % 计算结构相似性指标
    ssim_value = ((2 * mu_x * mu_y + k1) * (2 * cov_xy(1, 2) + k2)) / ...
        ((mu_x^2 + mu_y^2 + k1) * (sigma_x^2 + sigma_y^2 + k2));
end