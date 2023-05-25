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
    messageWindow()
    # tk.messagebox.showinfo('图片预览')


def dqn_button():
    # 将路径固定
    photo1_path = r"D:\pythonProject\UnfinishedBuilding\images\42049.jpg"
    photo2_path = r"D:\pythonProject\UnfinishedBuilding\images\43051.jpg"

    # 缩放后在界面显示
    photo1 = photo_resize(photo1_path)
    photo2 = photo_resize(photo2_path)
    photo_location(photo1, photo2)
    messageWindow()
    # tk.messagebox.showinfo('DQN算法边缘检测完成')

def messageWindow():
    win = tk.Toplevel()
    win.title('完成')
    message = "DQN算法边缘检测完成"
    tk.Label(win, text=message).pack(x=100, y=100)
    tk.Button(win, text='OK', command=win.destroy).pack()

# Button(root, text='Bring up Message', command=messageWindow).pack()


# 设置窗口
root = tk.Tk()
root.config(bg="#F2F1D7")
global WIDTH, HEIGHT, width, height
global save_path
WIDTH = 1050
HEIGHT = 550
width = 320
height = 200
save_path = r"D:\pythonProject\UnfinishedBuilding\images\finished\finished.png"

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

# "DQN"按钮
button8 = tk.Button(root, text='DQN算法', fg='#f00', bg='#DDF3FF', font=12, command=dqn_button, relief=tk.GROOVE, )
button8.place(x=920, y=20, width=110, height=32)

# 添加显示图片的Label
label_image = tk.Label(root, bg='#F2F1D7')
label_image1 = tk.Label(root, bg='#F2F1D7')
label_image2 = tk.Label(root, bg='#F2F1D7')

root.mainloop()