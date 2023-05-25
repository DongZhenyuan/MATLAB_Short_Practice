"""
命名约定：
GUI层面，图像数据的变量名为：Photo，所用函数来自PIL.Image
图像处理层面，图像数据的变量名为：img，所用函数来自cv2

选图要求：
尽量选择横板图片，且前景色和背景色对比强烈的。
原因：选横板是为了在窗口中显示的位置看起来端正；选前背景对比强烈的是为了较好的分割效果；

问题：
更新显示图片时，之前显示图片的位置会留下空白，遮挡之后显示的图片，看起来影响不大是因为选择横板图片时该现象并不明显，但这个问题始终未得到解决
"""
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

"""
该文件涉及图像处理和GUI用户界面制作
对于图像处理，主要依赖于cv2库和PIL库，二者都是常用的图像处理库，但在图像读入等处理上存在一些差异，并且产生的图像数据在彼此间不能直接通用
为此，用户可能需要编写一些“绕路”的代码。比如，在此我是将用cv2处理完的图片先保存到本地，再用Image读入再作处理。
对于图像的尺寸处理，通过Image.open(file_path)读入的图片可使用.size()方法计算长宽，而cv2.imread(file_path)读入的就不行
ImageTk.PhotoImage()对输入图片有格式上的要求(.png, .gif)。在这里，返回的结果用于：label_image.config(image=photo)

关于label_image.config()和tk.Label(root, image=img)的效果区别
label_image.config(image=photo)适用作标签中图片的更新；
imgLabel = tk.Label(root, image=img)则将图片整合到标签类中，适用作界面中几乎不作更改的图片(如背景)
来自select_botton()的示例：
    # 图片预览
    img = photo_resize(full_path)
    # imgLabel = tk.Label(root, image=img)
    # imgLabel.place(x=(WIDTH - photo_width) / 2, y=(HEIGHT - photo_heigh) / 2)
    # imgLabel.pack(side=tk.BOTTOM)
    # 以上两句的方法被弃用，虽然其作用和下方两句是一样的，但下述的用法似乎支持图片反复更新(经后来的试验，我也不那么确定了...)
    label_image.config(image=img)
    label_image.place(x=(WIDTH - width) / 2, y=(HEIGHT - height) / 2)
"""

def photo_resize(full_path):
    '''

    :param full_path: 从用户界面获取图片地址
    :return: 缩放后的图像长宽比为0.618，传入label_image.config()
    '''
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
    '''
    用于在窗口中定位两张图片
    :param photo1: 缩放后的原始图像
    :param photo2: 缩放后的边缘检测二值图像
    :return:
    '''
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
"""
明明是高度重复的行为，却写成多个函数。之所以采取饱受诟病的写法，原因如下：
Button类的command属性关联到单击按钮时执行的方法，但目前找到所有示例均无带参
Button(..., commond=methed(), ...)在处理存在实参传入的方法时会发生不符合期望的行为
"""
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
        cv2.imwrite(save_path, binary)
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
        cv2.imwrite(save_path, binary)
        # 缩放后在界面显示
        photo1 = photo_resize(full_path)
        photo2 = photo_resize(save_path)
        photo_location(photo1, photo2)
        tk.messagebox.showinfo('Prewitt算子边缘检测完成')

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
        cv2.imwrite(save_path, binary)
        # 缩放后在界面显示
        photo1 = photo_resize(full_path)
        photo2 = photo_resize(save_path)
        photo_location(photo1, photo2)
        tk.messagebox.showinfo('LOG算子边缘检测完成')

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
save_path = r"D:\z_UnfinishedBuilding\images\finished\finished.png"

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


# 算子逻辑与运算
button0 = tk.Button(root, text='Start', fg='#f00', bg='#DDF3FF', font=12, command=and_botton, relief=tk.GROOVE, )
button0.place(x=780, y=20, width=110, height=32)


# "sobel"按钮
button1 = tk.Button(root, text='sobel算子', fg='#f00', bg='#DDF3FF', font=12, command=sobel_button, relief=tk.GROOVE, )
button1.place(x=10, y=80, width=110, height=32)
# "canny"按钮
button2 = tk.Button(root, text='Canny算子', fg='#f00', bg='#DDF3FF', font=12, command=canny_button, relief=tk.GROOVE, )
button2.place(x=140, y=80, width=110, height=32)
# "Roberts"按钮
button3 = tk.Button(root, text='Roberts算子', fg='#f00', bg='#DDF3FF', font=12, command=robert_button, relief=tk.GROOVE, )
button3.place(x=270, y=80, width=110, height=32)
# "Prewitt"按钮
button4 = tk.Button(root, text='Prewitt算子', fg='#f00', bg='#DDF3FF', font=12, command=prewitt_button, relief=tk.GROOVE, )
button4.place(x=400, y=80, width=110, height=32)
# "Scharr"按钮
button5 = tk.Button(root, text='Scharr算子', fg='#f00', bg='#DDF3FF', font=12, command=scharr_button, relief=tk.GROOVE, )
button5.place(x=530, y=80, width=110, height=32)
# "Laplacian"按钮
button6 = tk.Button(root, text='Laplacian算子', fg='#f00', bg='#DDF3FF', font=12, command=laplacian_button, relief=tk.GROOVE, )
button6.place(x=660, y=80, width=110, height=32)
# "LOG"按钮
button7 = tk.Button(root, text='LOG算子', fg='#f00', bg='#DDF3FF', font=12, command=log_button, relief=tk.GROOVE, )
button7.place(x=790, y=80, width=110, height=32)
# "DQN"按钮
button8 = tk.Button(root, text='DQN算法', fg='#f00', bg='#DDF3FF', font=12, command=dqn_button, relief=tk.GROOVE, )
button8.place(x=920, y=80, width=110, height=32)


# 添加显示图片的Label
label_image = tk.Label(root, bg='#F2F1D7')
label_image1 = tk.Label(root, bg='#F2F1D7')
label_image2 = tk.Label(root, bg='#F2F1D7')
root.mainloop()
