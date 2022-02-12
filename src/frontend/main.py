from re import L
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
import pandas as pd

class Start(QDialog):
    def __init__(self):
        super(Start,self).__init__()
        loadUi("start.ui",self)
        self.crawlBtn.clicked.connect(self.crawlFunction)
        self.inputBtn.clicked.connect(self.inputFunction)

    def crawlFunction(self):
        crawl=Crawl()
        widget.addWidget(crawl)
        widget.setWindowTitle("Crawl data")
        widget.setCurrentIndex(widget.currentIndex()+1)

    def inputFunction(self):
        inputData=Input()
        widget.addWidget(inputData)
        widget.setWindowTitle("Nhập dữ liệu")
        widget.setCurrentIndex(widget.currentIndex()+1)

class Crawl(QDialog):
    def __init__(self):
        super(Crawl,self).__init__()
        loadUi("crawl.ui",self)
        self.setWindowTitle("Crawl dữ liệu")
        self.goBackBtn.clicked.connect(self.goBackFunction)
        self.crawlDataBtn.clicked.connect(self.crawlDataFunction)

    def goBackFunction(self):
        print('go back')
        goBack=Start()
        widget.addWidget(goBack)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def crawlDataFunction(self):
        stock = self.stockInput.text()
        print('stock', stock)
        advisory=Advisory()
        widget.addWidget(advisory)
        widget.setFixedWidth(1000)
        widget.setFixedHeight(730)
        widget.setWindowTitle("Tư vấn dữ liệu crawl")
        widget.setCurrentIndex(widget.currentIndex()+1)     

class Input(QDialog):
    def __init__(self):
        super(Input,self).__init__()
        loadUi("input.ui",self)
        self.setWindowTitle("Nhập dữ liệu")
        self.goBackBtn.clicked.connect(self.goBackFunction)

    def goBackFunction(self):
        print('go back')
        goBack=Start()
        widget.addWidget(goBack)
        widget.setCurrentIndex(widget.currentIndex()+1)
        widget.setFixedWidth(600)
        widget.setFixedHeight(300)


class Advisory(QDialog):
    def __init__(self):
        super(Advisory,self).__init__()
        loadUi("advisoryCrawl.ui",self)
        self.tableWidget.setColumnWidth(0,250)
        self.tableWidget.setColumnWidth(1,150)
        self.loadData()
        self.goBackBtn.clicked.connect(self.goBackFunction)

    def loadData(self):
        data = {
            "stock_code":"SSI",
            "RS_rating":"92",
            "AD_rating":"A+",
            "EPS_rating":"27",
            "SMR_rating":"A",
            "composite_rating":"93",
            "tien_cao_homnay":"45,050",
            "tien_thap_homnay":"43,200",
            "tien_thap_52T":"20,000",
            "tien_cao_52T":"55,900",
            "doanh_thu_quy_gan_nhat":"7,292,477",
            "doanh_thu_quy_gan_nhat_lien_ke":"4,366,801",
            "EPS_hom_nay":"1,955",
            "EPS_Q_gan_nhat":"3,651.00",
            "EPS_Q_gan_nhat_lien_ke":"2,178.00",
            "EPS_Q_gan_nhat_nam_truoc":"2,372.00",
            "EPS_Q_gan_nhat_lien_ke_nam_truoc":"1,826.00",
            "LNST_nam_gan_nhat":"2,671,974",
            "LNST_nam_truoc":"1,255,932",
            "LNST_nam_truoc_nua":"907,097",
            "ROE_nam_gan_nhat":"22.49",
            "ROE_nam_gan_nhat_lien_ke":"13.05"
        }

        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem("stock_code"))
        self.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(data["stock_code"]))

        self.tableWidget.setItem(1, 0, QtWidgets.QTableWidgetItem("RS_rating"))
        self.tableWidget.setItem(1, 1, QtWidgets.QTableWidgetItem(data["RS_rating"]))

        self.tableWidget.setItem(2, 0, QtWidgets.QTableWidgetItem("AD_rating"))
        self.tableWidget.setItem(2, 1, QtWidgets.QTableWidgetItem(data["AD_rating"]))

        self.tableWidget.setItem(3, 0, QtWidgets.QTableWidgetItem("EPS_rating"))
        self.tableWidget.setItem(3, 1, QtWidgets.QTableWidgetItem(data["EPS_rating"]))

        self.tableWidget.setItem(4, 0, QtWidgets.QTableWidgetItem("SMR_rating"))
        self.tableWidget.setItem(4, 1, QtWidgets.QTableWidgetItem(data["SMR_rating"]))

        self.tableWidget.setItem(5, 0, QtWidgets.QTableWidgetItem("composite_rating"))
        self.tableWidget.setItem(5, 1, QtWidgets.QTableWidgetItem(data["composite_rating"]))

        self.tableWidget.setItem(6, 0, QtWidgets.QTableWidgetItem("tien_cao_homnay"))
        self.tableWidget.setItem(6, 1, QtWidgets.QTableWidgetItem(data["tien_cao_homnay"]))

        self.tableWidget.setItem(7, 0, QtWidgets.QTableWidgetItem("tien_thap_homnay"))
        self.tableWidget.setItem(7, 1, QtWidgets.QTableWidgetItem(data["tien_thap_homnay"]))

        self.tableWidget.setItem(8, 0, QtWidgets.QTableWidgetItem("tien_thap_52T"))
        self.tableWidget.setItem(8, 1, QtWidgets.QTableWidgetItem(data["tien_thap_52T"]))

        self.tableWidget.setItem(9, 0, QtWidgets.QTableWidgetItem("tien_cao_52T"))
        self.tableWidget.setItem(9, 1, QtWidgets.QTableWidgetItem(data["tien_cao_52T"]))

        self.tableWidget.setItem(10, 0, QtWidgets.QTableWidgetItem("doanh_thu_quy_gan_nhat"))
        self.tableWidget.setItem(10, 1, QtWidgets.QTableWidgetItem(data["doanh_thu_quy_gan_nhat"]))

        self.tableWidget.setItem(11, 0, QtWidgets.QTableWidgetItem("doanh_thu_quy_gan_nhat_lien_ke"))
        self.tableWidget.setItem(11, 1, QtWidgets.QTableWidgetItem(data["doanh_thu_quy_gan_nhat_lien_ke"]))

        self.tableWidget.setItem(12, 0, QtWidgets.QTableWidgetItem("EPS_hom_nay"))
        self.tableWidget.setItem(12, 1, QtWidgets.QTableWidgetItem(data["EPS_hom_nay"]))

        self.tableWidget.setItem(13, 0, QtWidgets.QTableWidgetItem("EPS_Q_gan_nhat"))
        self.tableWidget.setItem(13, 1, QtWidgets.QTableWidgetItem(data["EPS_Q_gan_nhat"]))

        self.tableWidget.setItem(14, 0, QtWidgets.QTableWidgetItem("EPS_Q_gan_nhat_lien_ke"))
        self.tableWidget.setItem(14, 1, QtWidgets.QTableWidgetItem(data["EPS_Q_gan_nhat_lien_ke"]))

        self.tableWidget.setItem(15, 0, QtWidgets.QTableWidgetItem("EPS_Q_gan_nhat_nam_truoc"))
        self.tableWidget.setItem(15, 1, QtWidgets.QTableWidgetItem(data["EPS_Q_gan_nhat_nam_truoc"]))

        self.tableWidget.setItem(16, 0, QtWidgets.QTableWidgetItem("EPS_Q_gan_nhat_lien_ke_nam_truoc"))
        self.tableWidget.setItem(16, 1, QtWidgets.QTableWidgetItem(data["EPS_Q_gan_nhat_lien_ke_nam_truoc"]))

        self.tableWidget.setItem(17, 0, QtWidgets.QTableWidgetItem("LNST_nam_gan_nhat"))
        self.tableWidget.setItem(17, 1, QtWidgets.QTableWidgetItem(data["LNST_nam_gan_nhat"]))

        self.tableWidget.setItem(18, 0, QtWidgets.QTableWidgetItem("LNST_nam_truoc"))
        self.tableWidget.setItem(18, 1, QtWidgets.QTableWidgetItem(data["LNST_nam_truoc"]))

        self.tableWidget.setItem(19, 0, QtWidgets.QTableWidgetItem("LNST_nam_truoc_nua"))
        self.tableWidget.setItem(19, 1, QtWidgets.QTableWidgetItem(data["LNST_nam_truoc_nua"]))

        self.tableWidget.setItem(20, 0, QtWidgets.QTableWidgetItem("ROE_nam_gan_nhat"))
        self.tableWidget.setItem(20, 1, QtWidgets.QTableWidgetItem(data["ROE_nam_gan_nhat"]))

        self.tableWidget.setItem(21, 0, QtWidgets.QTableWidgetItem("ROE_nam_gan_nhat"))
        self.tableWidget.setItem(21, 1, QtWidgets.QTableWidgetItem(data["ROE_nam_gan_nhat_lien_ke"]))

    def goBackFunction(self):
        print('go back')
        goBack=Crawl()
        widget.addWidget(goBack)
        widget.setCurrentIndex(widget.currentIndex()+1)
        widget.setFixedWidth(600)
        widget.setFixedHeight(300)

    def advisoryFunction(self):
        self.advisoryLb = QLabel("Advisory label", self)

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])

app=QApplication(sys.argv)
mainwindow=Start()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(600)
widget.setFixedHeight(400)
widget.setWindowTitle("Dự đoán cổ phiếu")
widget.show()
app.exec_()