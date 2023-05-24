from AddDetails import AddDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox

import sys
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import re


class UiForm(QMainWindow):

    def select_path(self):
        path = os.getcwd()
        filename, a = QFileDialog.getOpenFileName(self, "选择文件", path, "png Files(*.png)")
        QFileDialog.setWindowIcon(self, QIcon('icon.png'))
        if filename == "":
            msg_box = QMessageBox(QMessageBox.Information, '提示', '未选择任何图片')
            msg_box.setWindowIcon(QIcon('icon.png'))
            msg_box.exec_()
        else:
            self.lineEdit.setText(filename)
            self.selected = 1

    def make_sure(self):
        if not self.selected:
            msg_box = QMessageBox(QMessageBox.Information, '提示', '未选择任何图片')
            msg_box.setWindowIcon(QIcon('icon.png'))
            msg_box.exec_()
            return
        # mainwindow.py中的其它函数都不重要，只是为了UI交互
        # 下面这句self.addDialog = AddDialog()才是核心；AddDialog()实例来自AddDetails.py，该类中调用模型dncnn_eval和my_eval
        self.addDialog = AddDialog()
        self.addDialog.pic_path = self.lineEdit.text()
        self.addDialog.show()

    def setup_ui(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        Form.setWindowIcon(QIcon('icon.png'))
        Form.setStyleSheet("#Form{border-image:url(img.png);}")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(345, 170, 320, 32))
        font = QtGui.QFont()
        font.setFamily("Freestyle Script")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(260, 220, 301, 40))
        self.lineEdit.setStyleSheet("\n"
                                    "QLineEdit {\n"
                                    "    border: 1px solid #A0A0A0; /* 边框宽度为1px，颜色为#A0A0A0 */\n"
                                    "    border-radius: 3px; /* 边框圆角 */\n"
                                    "    padding-left: 5px; /* 文本距离左边界有5px */\n"
                                    "    background-color: #F2F2F2; /* 背景颜色 */\n"
                                    "    color: #A0A0A0; /* 文本颜色 */\n"
                                    "    selection-background-color: #A0A0A0; /* 选中文本的背景颜色 */\n"
                                    "    selection-color: #F2F2F2; /* 选中文本的颜色 */\n"
                                    "    font-family: \"Microsoft YaHei\"; /* 文本字体族 */\n"
                                    "    font-size: 10pt; /* 文本字体大小 */\n"
                                    "}\n"
                                    "\n"
                                    "QLineEdit:hover { /* 鼠标悬浮在QLineEdit时的状态 */\n"
                                    "    border: 1px solid #298DFF;\n"
                                    "    border-radius: 3px;\n"
                                    "    background-color: #F2F2F2;\n"
                                    "    color: #298DFF;\n"
                                    "    selection-background-color: #298DFF;\n"
                                    "    selection-color: #F2F2F2;\n"
                                    "}\n"
                                    "\n"
                                    "QLineEdit[echoMode=\"2\"] { /* QLineEdit有输入掩码时的状态 */\n"
                                    "    lineedit-password-character: 9679;\n"
                                    "    lineedit-password-mask-delay: 2000;\n"
                                    "}\n"
                                    "\n"
                                    "QLineEdit:disabled { /* QLineEdit在禁用时的状态 */\n"
                                    "    border: 1px solid #CDCDCD;\n"
                                    "    background-color: #CDCDCD;\n"
                                    "    color: #B4B4B4;\n"
                                    "}\n"
                                    "\n"
                                    "QLineEdit:read-only { /* QLineEdit在只读时的状态 */\n"
                                    "    background-color: #CDCDCD;\n"
                                    "    color: #F2F2F2;\n"
                                    "}")
        self.lineEdit.setObjectName("lineEdit")
        self.select_button = QtWidgets.QPushButton(Form)
        self.select_button.setGeometry(QtCore.QRect(260, 300, 140, 40))
        self.select_button.setStyleSheet("border-radius: 5px;\n"
                                         "border: 2px solid black")
        self.select_button.setText("选择图像")
        self.select_button.clicked.connect(self.select_path)

        self.generate_button = QtWidgets.QPushButton(Form)
        self.generate_button.setGeometry(QtCore.QRect(420, 300, 140, 40))
        self.generate_button.setStyleSheet("border-radius: 5px;\n"
                                           "border: 2px solid black")
        self.generate_button.setText("开始去噪")
        self.generate_button.clicked.connect(self.make_sure)
        self.selected = 0

        # self.pushButton.setObjectName("pushButton")
        self.retranslate_ui(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslate_ui(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "图像去噪"))
        self.label.setText(_translate("Form", "请输入图像路径"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = QtWidgets.QMainWindow()
    ui = UiForm()
    ui.setup_ui(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())
