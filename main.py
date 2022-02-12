from re import L
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from src.frontend.ui import Main

app = QApplication(sys.argv)
mainwindow = Main()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1400)
widget.setFixedHeight(810)
widget.setWindowTitle("Dự đoán cổ phiếu")
widget.show()
app.exec_()
