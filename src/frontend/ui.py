from re import I, L
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
import pandas as pd
from src.crawl import solve
from src.database import find_all_rules
from src.rules import insert_new_rule, update_new_rule, delete_rule
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtWidgets import QMainWindow, QWidget, QPlainTextEdit

class Main(QDialog):
    def __init__(self):
        super(Main,self).__init__()
        loadUi("src/frontend/main.ui",self)
        self.crawlBtn.clicked.connect(self.loadCrawlDataFunction)
        self.advisoryBtn.clicked.connect(self.advisoryFunction)
        self.addRuleBtn.clicked.connect(self.addRuleFunction)
        self.updateBtn.clicked.connect(self.updateRuleFunction)
        self.deleteBtn.clicked.connect(self.deleteRuleFunction)
        self.loadRule()
        self.ruleTbl.clicked.connect(self.getItemFunction)

    def loadRule(self):
        print('load rule')
        docs = find_all_rules()
        self.ruleTbl.setRowCount(len(docs))
        self.ruleTbl.setColumnWidth(0, 385)
        self.ruleTbl.setColumnWidth(1, 100)
        self.ruleTbl.setColumnWidth(2, 100)
        self.ruleTbl.setColumnWidth(3, 100)
        i = 0
        conditionStr = ''
        for doc in docs:
            print(doc["_id"])
            self.ruleTbl.setItem(i, 0, QtWidgets.QTableWidgetItem(doc["_id"]))
            self.ruleTbl.setItem(i, 1, QtWidgets.QTableWidgetItem(doc["name"]))
            self.ruleTbl.setItem(i, 2, QtWidgets.QTableWidgetItem(doc["description"]))
            self.ruleTbl.setItem(i, 3, QtWidgets.QTableWidgetItem(doc["value"]))
            for condition in doc["conditions"]:
                conditionStr = condition[0] + ' ' 
            self.ruleTbl.setItem(i, 4, QtWidgets.QTableWidgetItem(conditionStr))
            i+= 1
        print(docs)
    
    def getItemFunction(self):
        print('get item')
        row = self.ruleTbl.currentRow()
        col = self.ruleTbl.currentColumn()
        # text = self.ruleTbl.item(row, col).text()
        # print('row ', row)
        # print('col ', col)
        # print(text)
        rowItemId = self.ruleTbl.item(row,0).text()
        rowItemName= self.ruleTbl.item(row,1).text()
        rowItemDes= self.ruleTbl.item(row,2).text()
        rowItemValue= self.ruleTbl.item(row,3).text()
        rowItemCondition= self.ruleTbl.item(row,4).text()
        return rowItemId,rowItemName,rowItemDes,rowItemValue,rowItemCondition

    def loadCrawlDataFunction(self):
        data = solve(self.stockInput.text())

        self.dataTbl.setRowCount(len(data))
        self.dataTbl.setColumnWidth(0, 300)
        self.dataTbl.setColumnWidth(1, 166)
        self.dataTbl.setItem(0, 0, QtWidgets.QTableWidgetItem("stock_code"))
        self.dataTbl.setItem(0, 1, QtWidgets.QTableWidgetItem(data["stock_code"]))

        self.dataTbl.setItem(1, 0, QtWidgets.QTableWidgetItem("RS_rating"))
        self.dataTbl.setItem(1, 1, QtWidgets.QTableWidgetItem(data["RS_rating"]))

        self.dataTbl.setItem(2, 0, QtWidgets.QTableWidgetItem("AD_rating"))
        self.dataTbl.setItem(2, 1, QtWidgets.QTableWidgetItem(data["AD_rating"]))

        self.dataTbl.setItem(3, 0, QtWidgets.QTableWidgetItem("EPS_rating"))
        self.dataTbl.setItem(3, 1, QtWidgets.QTableWidgetItem(data["EPS_rating"]))

        self.dataTbl.setItem(4, 0, QtWidgets.QTableWidgetItem("SMR_rating"))
        self.dataTbl.setItem(4, 1, QtWidgets.QTableWidgetItem(data["SMR_rating"]))

        self.dataTbl.setItem(5, 0, QtWidgets.QTableWidgetItem("composite_rating"))
        self.dataTbl.setItem(5, 1, QtWidgets.QTableWidgetItem(data["composite_rating"]))

        self.dataTbl.setItem(6, 0, QtWidgets.QTableWidgetItem("tien_cao_homnay"))
        self.dataTbl.setItem(6, 1, QtWidgets.QTableWidgetItem(data["tien_cao_homnay"]))

        self.dataTbl.setItem(7, 0, QtWidgets.QTableWidgetItem("tien_thap_homnay"))
        self.dataTbl.setItem(7, 1, QtWidgets.QTableWidgetItem(data["tien_thap_homnay"]))

        self.dataTbl.setItem(8, 0, QtWidgets.QTableWidgetItem("tien_thap_52T"))
        self.dataTbl.setItem(8, 1, QtWidgets.QTableWidgetItem(data["tien_thap_52T"]))

        self.dataTbl.setItem(9, 0, QtWidgets.QTableWidgetItem("tien_cao_52T"))
        self.dataTbl.setItem(9, 1, QtWidgets.QTableWidgetItem(data["tien_cao_52T"]))

        self.dataTbl.setItem(10, 0, QtWidgets.QTableWidgetItem("doanh_thu_quy_gan_nhat"))
        self.dataTbl.setItem(10, 1, QtWidgets.QTableWidgetItem(data["doanh_thu_quy_gan_nhat"]))

        self.dataTbl.setItem(11, 0, QtWidgets.QTableWidgetItem("doanh_thu_quy_gan_nhat_lien_ke"))
        self.dataTbl.setItem(11, 1, QtWidgets.QTableWidgetItem(data["doanh_thu_quy_gan_nhat_lien_ke"]))

        self.dataTbl.setItem(12, 0, QtWidgets.QTableWidgetItem("EPS_hom_nay"))
        self.dataTbl.setItem(12, 1, QtWidgets.QTableWidgetItem(data["EPS_hom_nay"]))

        self.dataTbl.setItem(13, 0, QtWidgets.QTableWidgetItem("EPS_Q_gan_nhat"))
        self.dataTbl.setItem(13, 1, QtWidgets.QTableWidgetItem(data["EPS_Q_gan_nhat"]))

        self.dataTbl.setItem(14, 0, QtWidgets.QTableWidgetItem("EPS_Q_gan_nhat_lien_ke"))
        self.dataTbl.setItem(14, 1, QtWidgets.QTableWidgetItem(data["EPS_Q_gan_nhat_lien_ke"]))

        self.dataTbl.setItem(15, 0, QtWidgets.QTableWidgetItem("EPS_Q_gan_nhat_nam_truoc"))
        self.dataTbl.setItem(15, 1, QtWidgets.QTableWidgetItem(data["EPS_Q_gan_nhat_nam_truoc"]))

        self.dataTbl.setItem(16, 0, QtWidgets.QTableWidgetItem("EPS_Q_gan_nhat_lien_ke_nam_truoc"))
        self.dataTbl.setItem(16, 1, QtWidgets.QTableWidgetItem(data["EPS_Q_gan_nhat_lien_ke_nam_truoc"]))

        self.dataTbl.setItem(17, 0, QtWidgets.QTableWidgetItem("LNST_nam_gan_nhat"))
        self.dataTbl.setItem(17, 1, QtWidgets.QTableWidgetItem(data["LNST_nam_gan_nhat"]))

        self.dataTbl.setItem(18, 0, QtWidgets.QTableWidgetItem("LNST_nam_truoc"))
        self.dataTbl.setItem(18, 1, QtWidgets.QTableWidgetItem(data["LNST_nam_truoc"]))

        self.dataTbl.setItem(19, 0, QtWidgets.QTableWidgetItem("LNST_nam_truoc_nua"))
        self.dataTbl.setItem(19, 1, QtWidgets.QTableWidgetItem(data["LNST_nam_truoc_nua"]))

        self.dataTbl.setItem(20, 0, QtWidgets.QTableWidgetItem("ROE_nam_gan_nhat"))
        self.dataTbl.setItem(20, 1, QtWidgets.QTableWidgetItem(data["ROE_nam_gan_nhat"]))

        self.dataTbl.setItem(21, 0, QtWidgets.QTableWidgetItem("ROE_nam_gan_nhat"))
        self.dataTbl.setItem(21, 1, QtWidgets.QTableWidgetItem(data["ROE_nam_gan_nhat_lien_ke"]))

    def advisoryFunction(self):
        self.resultLb.setText("AloAlo")
        self.resultLb.setAlignment(Qt.AlignCenter)

    def addRuleFunction(self):
        print('create')
        create=Create()
        widget.addWidget(create)
        widget.setFixedWidth(600)
        widget.setFixedHeight(600)
        widget.setWindowTitle("Thêm tập luật")
        widget.setCurrentIndex(widget.currentIndex()+1)    

    def updateRuleFunction(self):
        print('update')
        rowItemId,rowItemName,rowItemDes,rowItemValue,rowItemCondition = self.getItemFunction()
        update_new_rule(rowItemId,rowItemName,rowItemDes,rowItemValue,rowItemCondition)
        self.loadRule()

    def deleteRuleFunction(self):
        print('delete')
        rowItemId,rowItemName,rowItemDes,rowItemValue,rowItemCondition = self.getItemFunction()
        delete_rule(rowItemId)
        self.loadRule()

class Create(QDialog):
    def __init__(self):
        super(Create,self).__init__()
        loadUi("src/frontend/createRule.ui",self)
        self.goBackBtn.clicked.connect(self.goBackFunction)
        self.createRuleBtn.clicked.connect(self.createRuleFunction)
        self.ruleInput = QPlainTextEdit(self)
        self.ruleInput.move(45, 235)
        self.ruleInput.resize(500,250)

    def goBackFunction(self):
        print('go back')
        goBack=Main()
        widget.addWidget(goBack)
        widget.setFixedWidth(1400)
        widget.setFixedHeight(810)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def createRuleFunction(self):
        print('createRule')
        try:
            rule_new = insert_new_rule(self.nameInput.text(), self.descriptionInput.text(), self.valueInput.text(), self.ruleInput.toPlainText())
            self.nameInput.clear()
            self.descriptionInput.clear()
            self.valueInput.clear()
            self.ruleInput.clear()
        except:
            print('failed')

    def deleteRuleFunction(self):
        print('')

app=QApplication(sys.argv)
mainwindow=Main()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1400)
widget.setFixedHeight(810)
widget.setWindowTitle("Dự đoán cổ phiếu")
widget.show()
app.exec_()