
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.filedialog    # 用于选择文件以及获取所取文件的路径
import tkinter.messagebox

import cv2

from sobel import sobel
from canny import canny
from robert import roberts
from prewitt import prewitt
from scharr import scharr
from laplacian import laplacian
from LOG import LOG


def photo_resize(full_path):
    photo = Image.open(full_path)
    photo_width = photo.size[0]
    photo_heigh = photo.size[1]
    # 图片缩放
    if photo_width > photo_heigh:
        photo_heigh = int(photo_heigh * width / photo_width)
        photo_width = width
    else:
        photo_width = int(photo_width * height / photo_heigh)
        photo_heigh = height
    out = photo.resize((photo_width, photo_heigh))
    return ImageTk.PhotoImage(out)

def photo_location(photo1, photo2):
    label_image1.config(image=photo1)
    label_image1.place(x=(WIDTH / 2 - width) / 2, y=HEIGHT / 3)
    label_image2.config(image=photo2)
    label_image2.place(x=(3 * WIDTH / 2 - width) / 2, y=HEIGHT / 3)

def select_botton():
    global full_path
    fileType = [('jpg文件', '*.jpg'), ('png文件', '*.png'), ]
    # 获取目标图片的地址
    full_path = tk.filedialog.askopenfilename(title='选择图片', filetypes=fileType)
    # 图片预览
    img = photo_resize(full_path)
    label_image.config(image=img)
    label_image.place(x=(WIDTH - width) / 2, y=(HEIGHT - height) / 2)
    txt.set(full_path)
    tk.messagebox.showinfo('图片预览')

# ----------------------------------------边缘检测---------------------------------------- #
# ----------------------------------------Sobel算子---------------------------------------- #
def sobel_button():
    full_path = txt.get()
    if full_path == '':
        tk.messagebox.showerror('错误', '所选文件为空，请重新选择')
    else:
        # 将原始图像转化为灰度图，作为待处理图形
        pending_img = cv2.imread(full_path, 0)
        finished_img = sobel(pending_img)
        # 对边缘检测后返回的图像进行二值化处理
        _, binary = cv2.threshold(finished_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # 将结果保存到本地
        cv2.imwrite(save_path, finished_img)
        # 缩放后在界面显示
        photo1 = photo_resize(full_path)
        photo2 = photo_resize(save_path)
        photo_location(photo1, photo2)
        tk.messagebox.showinfo('Sobel算子边缘检测完成')

# ----------------------------------------Canny算子---------------------------------------- #
def canny_button():
    full_path = txt.get()
    if full_path == '':
        tk.messagebox.showerror('错误', '所选文件为空，请重新选择')
    else:
        # 将原始图像转化为灰度图，作为待处理图形
        pending_img = cv2.imread(full_path, 0)
        finished_img = canny(pending_img)
        # 对边缘检测后返回的图像进行二值化处理
        _, binary = cv2.threshold(finished_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # 将结果保存到本地
        cv2.imwrite(save_path, binary)
        # 缩放后在界面显示
        photo1 = photo_resize(full_path)
        photo2 = photo_resize(save_path)
        photo_location(photo1, photo2)
        tk.messagebox.showinfo('Canny算子边缘检测完成')

# ----------------------------------------Robert算子---------------------------------------- #
def robert_button():
    full_path = txt.get()
    if full_path == '':
        tk.messagebox.showerror('错误', '所选文件为空，请重新选择')
    else:
        # 将原始图像转化为灰度图，作为待处理图形
        pending_img = cv2.imread(full_path, 0)
        finished_img = roberts(pending_img)
        # 对边缘检测后返回的图像进行二值化处理
        _, binary = cv2.threshold(finished_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # 将结果保存到本地
        cv2.imwrite(save_path, binary)
        # 缩放后在界面显示
        photo1 = photo_resize(full_path)
        photo2 = photo_resize(save_path)
        photo_location(photo1, photo2)
        tk.messagebox.showinfo('Robert算子边缘检测完成')

# ----------------------------------------Prewitt算子---------------------------------------- #
def prewitt_button():
    full_path = txt.get()
    if full_path == '':
        tk.messagebox.showerror('错误', '所选文件为空，请重新选择')
    else:
        # 将原始图像转化为灰度图，作为待处理图形
        pending_img = cv2.imread(full_path, 0)
        finished_img = prewitt(pending_img)
        # 对边缘检测后返回的图像进行二值化处理
        _, binary = cv2.threshold(finished_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # 将结果保存到本地
        cv2.imwrite(save_path, finished_img)
        # 缩放后在界面显示
        photo1 = photo_resize(full_path)
        photo2 = photo_resize(save_path)
        photo_location(photo1, photo2)
        tk.messagebox.showinfo('Laplacian算子边缘检测完成')

# ----------------------------------------Scharr算子---------------------------------------- #
def scharr_button():
    full_path = txt.get()
    if full_path == '':
        tk.messagebox.showerror('错误', '所选文件为空，请重新选择')
    else:
        # 将原始图像转化为灰度图，作为待处理图形
        pending_img = cv2.imread(full_path, 0)
        finished_img = scharr(pending_img)
        # 对边缘检测后返回的图像进行二值化处理
        _, binary = cv2.threshold(finished_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # 将结果保存到本地
        cv2.imwrite(save_path, binary)
        # 缩放后在界面显示
        photo1 = photo_resize(full_path)
        photo2 = photo_resize(save_path)
        photo_location(photo1, photo2)
        tk.messagebox.showinfo('Scharr算子边缘检测完成')

# ----------------------------------------Laplacian算子---------------------------------------- #
def laplacian_button():
    full_path = txt.get()
    if full_path == '':
        tk.messagebox.showerror('错误', '所选文件为空，请重新选择')
    else:
        # 将原始图像转化为灰度图，作为待处理图形
        pending_img = cv2.imread(full_path)
        finished_img = laplacian(pending_img)
        # 对边缘检测后返回的图像进行二值化处理
        _, binary = cv2.threshold(finished_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # 将结果保存到本地
        cv2.imwrite(save_path, binary)
        # 缩放后在界面显示
        photo1 = photo_resize(full_path)
        photo2 = photo_resize(save_path)
        photo_location(photo1, photo2)
        tk.messagebox.showinfo('Laplacian算子边缘检测完成')

# ----------------------------------------LOG算子---------------------------------------- #
def log_button():
    full_path = txt.get()
    if full_path == '':
        tk.messagebox.showerror('错误', '所选文件为空，请重新选择')
    else:
        # 将原始图像转化为灰度图，作为待处理图形
        pending_img = cv2.imread(full_path, 0)
        finished_img = LOG(pending_img)
        # 对边缘检测后返回的图像进行二值化处理
        _, binary = cv2.threshold(finished_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # 将结果保存到本地
        cv2.imwrite(save_path, finished_img)
        # 缩放后在界面显示
        photo1 = photo_resize(full_path)
        photo2 = photo_resize(save_path)
        photo_location(photo1, photo2)
        tk.messagebox.showinfo('Canny算子边缘检测完成')

# ----------------------------------------DQN算法---------------------------------------- #
def dqn_button():
    # 将路径固定
    photo1_path = r"D:\pythonProject\UnfinishedBuilding\images\42049.jpg"
    photo2_path = r"D:\pythonProject\UnfinishedBuilding\images\43051.jpg"

    # 缩放后在界面显示
    photo1 = photo_resize(photo1_path)
    photo2 = photo_resize(photo2_path)
    photo_location(photo1, photo2)
    tk.messagebox.showinfo('DQN算法边缘检测完成')

# ----------------------------------------算子与运算---------------------------------------- #
def and_botton():
    full_path = txt.get()
    if full_path == '':
        tk.messagebox.showerror('错误', '所选文件为空，请重新选择')
    else:
        # 将原始图像转化为灰度图，作为待处理图形
        pending_img = cv2.imread(full_path, 0)
        # 这里选择了sobel、canny和laplacian3种算子的分割图
        finished_img1 = sobel(pending_img)
        finished_img2 = canny(pending_img)
        finished_img3 = laplacian(pending_img)
        # 对边缘检测后返回的图像进行二值化处理
        _, binary1 = cv2.threshold(finished_img1, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        _, binary2 = cv2.threshold(finished_img2, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        _, binary3 = cv2.threshold(finished_img3, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # 二值图的逻辑与运算
        '''二值图的元素只有0和255，这里使用了数组乘法作为与运算，255*255*255的结果居然是255，而非255^3，正合我意'''
        binary = binary1 * binary2 * binary3
        # 将结果保存到本地
        cv2.imwrite(save_path, binary)
        # 缩放后在界面显示
        photo1 = photo_resize(full_path)
        photo2 = photo_resize(save_path)
        photo_location(photo1, photo2)
        tk.messagebox.showinfo('DQN边缘检测完成')


# 设置窗口
root = tk.Tk()
root.config(bg="#F2F1D7")
global WIDTH, HEIGHT, width, height
global save_path
WIDTH = 1050
HEIGHT = 550
width = 320
height = 200
save_path = r"C:\Users\gcx\Desktop\pythonProject\finished\finished.png"


root.geometry(f'{WIDTH}x{HEIGHT}')
root.title('边缘检测算法选择')

# 设置主循环
label1 = tk.Label(root, text='choose the photo', font=("bold", 14), fg='#f00', bg='#F2F1D7')
label1.place(x=20, y=25)
txt = tk.StringVar()
txt_entry = tk.Entry(root, width=55, textvariable=txt, relief=tk.GROOVE)
txt_entry.place(x=220, y=20, width=400, height=30)

# "浏览"按钮
button = tk.Button(root, text='browse', fg='#f00', bg='#E8FFE8', font=14, command=select_botton, relief=tk.GROOVE, )
button.place(x=680, y=20, width=60, height=32)



# "sobel"按钮
button1 = tk.Button(root, text='sobel算子', fg='#f00', bg='#DDF3FF', font=12, command=sobel_button, relief=tk.GROOVE, )
button1.place(x=10, y=80, width=110, height=32)
# "canny"按钮
button2 = tk.Button(root, text='Canny算子', fg='#f00', bg='#DDF3FF', font=12, command=log_button, relief=tk.GROOVE, )
button2.place(x=140, y=80, width=110, height=32)
# "Roberts"按钮
button3 = tk.Button(root, text='Laplacian算子', fg='#f00', bg='#DDF3FF', font=12, command=prewitt_button, relief=tk.GROOVE, )
button3.place(x=270, y=80, width=110, height=32)


# 添加显示图片的Label
label_image = tk.Label(root, bg='#F2F1D7')
label_image1 = tk.Label(root, bg='#F2F1D7')
label_image2 = tk.Label(root, bg='#F2F1D7')

root.mainloop()