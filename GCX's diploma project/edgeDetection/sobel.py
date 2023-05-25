import numpy as np

def sobel(img):
    h,w=img.shape
    new_img=np.zeros([h,w])
    x_img=np.zeros(img.shape)
    y_img=np.zeros(img.shape)
    sobel_x=np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    sobel_y=np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
    for i in range(h-2):
        for j in range(w-2):
            x_img[i+1,j+1]=abs(np.sum(img[i:i+3,j:j+3]*sobel_x))
            y_img[i+1,j+1]=abs(np.sum(img[i:i+3,j:j+3]*sobel_y))
            new_img[i+1,j+1]=np.sqrt(np.square(x_img[i+1,j+1])+np.square(y_img[i+1,j+1]))

    return np.uint8(new_img)

