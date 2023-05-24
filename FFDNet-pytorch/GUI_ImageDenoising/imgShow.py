"""
该界面用于呈现图像的去噪效果
效果是显示一个窗口，并提供保存图片的功能
"""
import os
import sys
import re
import PyQt5
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import myModel
import cv2


class Table(QWidget):

    def __init__(self, cols):
        super().__init__()
        self.cols = cols
        self.init_ui()
        # 如果cols的值为3，则将名为chuizhi_layout_3的布局添加到名为shuiping_layout的布局中。
        if self.cols == 3:
            self.shuiping_layout.addLayout(self.chuizhi_layout_3)

    def save_pic(self, pic_path):
        """
        保存图片  pic_path图片路径  file_path保存图片路径
        """
        if os.path.exists(pic_path):
            file_path = QFileDialog.getSaveFileName(self, "保存文件夹", pic_path, '')[0]
            if file_path == '':
                # 创建一个消息框msg_box，其中QMessageBox.Information表示消息框的类型为信息提示框，
                # '提示'是消息框的标题，'未选择路径！'是消息框的文本内容。
                msg_box = QMessageBox(QMessageBox.Information, '提示', '未选择路径！')
                msg_box.setWindowIcon(QIcon('pic/tubiao.png'))
                msg_box.exec_()
                return
            # file_path不为空字符串
            # imread函数读取图片文件，将其保存为img。imwrite函数将img保存到指定路径file_path。
            img = cv2.imread(pic_path)
            cv2.imwrite(file_path, img)
            msg_box = QMessageBox(QMessageBox.Information, '提示', '保存成功！')
            msg_box.setWindowIcon(QIcon('icon.png'))
            msg_box.exec_()

    def init_ui(self):
        """
        界面初始化的方法，用于设置窗口的标题、图标、大小以及布局
        :return:
        """
        self.setWindowTitle("降噪结果")
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(1200, 900)
        # 创建一个水平布局对象shuiping_layout。
        self.shuiping_layout = QHBoxLayout()
        self.chuizhi_layout_1 = QVBoxLayout()
        self.chuizhi_layout_2 = QVBoxLayout()
        self.chuizhi_layout_3 = QVBoxLayout()

        HbottonStyle = '''/**正常情况下样式**/
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
        # 创建另存为按钮
        self.save_button1 = QPushButton()
        self.save_button1.setText("另存为")
        self.save_button1.resize(100, 30)
        self.save_button1.setStyleSheet(HbottonStyle)
        self.save_button1.clicked.connect(lambda: self.save_pic('original.png'))

        # 创建一个名为pic_lable1的QLabel实例，用于显示图片。
        self.pic_lable1 = QLabel()
        self.text1 = QPushButton()
        self.text1.setText("原图像")
        self.text1.resize(100, 30)
        self.text1.setEnabled(False)
        self.text1.setStyleSheet(HbottonStyle)

        self.pic_lable2 = QLabel()
        self.text2 = QPushButton()
        self.text2.setText("本文方法降噪图像")
        self.text2.resize(100, 30)
        self.text2.setEnabled(False)
        self.text2.setStyleSheet(HbottonStyle)

        self.pic_lable3 = QLabel()
        self.text3 = QPushButton()
        self.text3.setText("DnCnn降噪图像")
        self.text3.resize(100, 30)
        self.text3.setEnabled(False)
        self.text3.setStyleSheet(HbottonStyle)

        self.save_button2 = QPushButton()
        self.save_button2.setText("另存为")
        self.save_button2.resize(100, 30)
        self.save_button2.setStyleSheet(HbottonStyle)
        self.save_button2.clicked.connect(lambda: self.save_pic('my_model.png'))
        self.save_button3 = QPushButton()
        self.save_button3.setText("另存为")
        self.save_button3.resize(100, 30)
        self.save_button3.setStyleSheet(HbottonStyle)
        self.save_button3.clicked.connect(lambda: self.save_pic('dncnn.png'))

        # 将之前创建的按钮和标签添加到布局中
        self.chuizhi_layout_1.addWidget(self.text1)
        self.chuizhi_layout_1.addWidget(self.pic_lable1)
        self.chuizhi_layout_1.addWidget(self.save_button1)
        self.chuizhi_layout_2.addWidget(self.text2)
        self.chuizhi_layout_2.addWidget(self.pic_lable2)
        self.chuizhi_layout_2.addWidget(self.save_button2)
        self.chuizhi_layout_3.addWidget(self.text3)
        self.chuizhi_layout_3.addWidget(self.pic_lable3)
        self.chuizhi_layout_3.addWidget(self.save_button3)
        self.shuiping_layout.addLayout(self.chuizhi_layout_1)
        self.shuiping_layout.addLayout(self.chuizhi_layout_2)

        # 设置背景
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("img.png")))
        # self.setPalette(palette)
        self.setLayout(self.shuiping_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = Table(2)
    example.show()
    sys.exit(app.exec_())

