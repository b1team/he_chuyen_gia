from src.log import setup_logging
from config import LOG_LEVEL

setup_logging(name="src", level=LOG_LEVEL)

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
