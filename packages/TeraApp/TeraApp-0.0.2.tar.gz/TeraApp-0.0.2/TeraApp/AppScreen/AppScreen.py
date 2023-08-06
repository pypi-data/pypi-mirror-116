from PyQt5.QtWidgets import QLabel
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import *
import sys


class TeraApp:
  def __init__(self, title, x, y, colorbg):
    self.app = QtWidgets.QApplication(sys.argv)
    self.win = QtWidgets.QMainWindow()
    self.win.setWindowTitle(title)
    self.win.setGeometry(500, 200, x, y)
    self.win.setStyleSheet(f"background-color: {colorbg};")

    self.win.show()


  def txt(self,txt, x, y, size):
    txt_name = QtWidgets.QLabel(self.win)
    txt_name.setText(txt)
    txt_name.move(x, y)
    txt_name.setFont(QFont('Arial', size))
    txt_name.show()

  def button(self, txt, x, y, colorbg):
    button = QtWidgets.QPushButton(self.win)
    button.setText(txt)
    button.move(x,y)
    button.setStyleSheet(f"background-color: {colorbg};")
    button.show()

  def buttonf(self, txt, x, y, colorbg, function):
    buttonf = QtWidgets.QPushButton(self.win)
    buttonf.setText(txt)
    buttonf.move(x, y)
    buttonf.setStyleSheet(f"background-color: {colorbg};")
    buttonf.clicked.connect(function)
    buttonf.show()

  def img2(self, img, x, y):
    im = QPixmap(f"{img}").scaledToHeight(60)
    label = QLabel(self.win)
    label.setPixmap(im)
    label.move(x, y)
    label.show()

  def img(self, img, x, y, size_x, size_y):
    label = QtWidgets.QLabel(self.win)
    label.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
    label.resize(size_x,size_y)
    label.setContentsMargins(0,0,0,0)
    pixmap = QtGui.QPixmap(f'{img}')
    label.setPixmap(pixmap)
    label.setMinimumSize(1,1)
    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(label)
    label.move(x, y)
    label.show()

  def icon(self, img, x, y):
    im = QPixmap(f"{img}").scaledToHeight(36)
    label = QLabel(self.win)
    label.setPixmap(im)
    label.move(x, y)
    label.show()

  def input(self, x, y, colorbg):
    input_name = QtWidgets.QLineEdit(self.win)
    input_name.move(x, y)
    input_name.setStyleSheet(f"background-color: {colorbg};")
    input_name.show()






