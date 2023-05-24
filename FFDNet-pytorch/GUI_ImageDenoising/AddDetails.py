import cv2
import sys
import os
import time
from PyQt5.QtWidgets import QVBoxLayout

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from imgShow import Table
from dnCnn import dncnn_eval
from myModel import my_eval


class AddDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.bottonStyle = '''/**正常情况下样式**/
                QPushButton{
                	font: 10pt "微软雅黑";
                    color: #2f3640;
                    background-color: #f5f6fa;
                    border-color: #2f3640;
                    border-radius: 15px;
                    border-style: solid;
                    border-width: 2px;
                    padding: 5px;
                }

                /**鼠标停留在按钮上的样式**/
                QPushButton::hover{	
                    color: #FFFFFF;
                    background-color: #718093;
                    border-color: #2f3640;
                }

                /**鼠标按压下去的样式**/
                QPushButton::pressed,QPushButton::checked{
                    color: #FFFFFF;
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #273c75, stop:1 #487eb0);
                }

                /**按钮失能情况下样式**/
                QPushButton::disabled{
                    color: #000000;
                    background-color: #dcdde1;
                    border-color: #dcdde1;
                }'''
        self.init_ui()

    def pic_reshape(self, img_path):
        img = cv2.imread(img_path)
        size = 400
        height, width = img.shape[0], img.shape[1]
        scale = width / size
        height_size = int(height / scale)
        # cv2.resize(img, (图片的宽, 图片的高))
        img = cv2.resize(img, (size, height_size))
        cv2.imwrite('original.png', img)

    def init_ui(self):

        '''水平布局'''
        self.resize(400,200)

        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle("设置详细信息")
        self.save_btn = QPushButton()
        self.save_btn.setText('确认')
        self.save_btn.clicked.connect(self.save_btn_click)
        self.save_btn.setStyleSheet(self.bottonStyle)
        self.cancel_btn = QPushButton()
        self.cancel_btn.setText('取消')
        self.cancel_btn.clicked.connect(self.cancel_btn_click)
        self.cancel_btn.setStyleSheet(self.bottonStyle)


        # 表单布局
        self.section_lab = QLabel()
        self.section_lab.setText("选择去噪方法:")
        self.section_select = QComboBox()
        self.section_select.addItem('改进的DnCnn')
        self.section_select.addItem('DnCNN对比本文方法')

        self.first_line = QHBoxLayout()

        self.third_line = QHBoxLayout()
        self.third_line.addWidget(self.section_lab)
        self.third_line.addWidget(self.section_select)

        self.fourth_line = QHBoxLayout()
        self.fourth_line.addWidget(self.save_btn)
        self.fourth_line.addWidget(self.cancel_btn)

        self.vbox = QVBoxLayout()
        # self.vbox.addLayout(self.first_line)
        # self.vbox.addLayout(self.second_line)
        self.vbox.addLayout(self.third_line)
        # self.vbox.addWidget(self.Table)
        self.vbox.addLayout(self.fourth_line)
        self.setLayout(self.vbox)

    def save_btn_click(self):
        self.pic_reshape(self.pic_path)
        if self.section_select.currentText() == '改进的DnCnn':
            self.table = Table(2)

        else:
            self.table = Table(3)
        self.close()
        self.pix1 = QPixmap("original.png")
        self.table.pic_lable1.setPixmap(self.pix1)
        self.table.show()

        # 重点来了，FFDNet模型评估在这里
        my_eval("original.png", "my_model.png")
        self.pix2 = QPixmap("my_model.png")
        self.table.pic_lable2.setPixmap(self.pix2)
        if self.section_select.currentText() != '改进的DnCNN':
            # DnCNN模型评估在这里
            dncnn_eval("original.png", "dncnn.png")
            self.pix3 = QPixmap("dncnn.png")
            self.table.pic_lable3.setPixmap(self.pix3)

    def cancel_btn_click(self):
        self.close()

    # @staticmethod
    # def get_add_dialog(parent=None):
    #     dialog = AddDialog(parent)
    #     return dialog.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = AddDialog()
    example.show()
    sys.exit(app.exec_())