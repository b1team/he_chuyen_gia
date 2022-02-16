from re import I, L
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPlainTextEdit, QVBoxLayout,QMainWindow, QWidget, QPlainTextEdit,QLabel, QTableWidget,QHeaderView,QTableWidgetItem, QPushButton, QLineEdit
import pandas as pd
from src.crawl import solve
from src.database import find_all_rules
from src.rules import insert_new_rule, update_new_rule, delete_rule,parse_rules_conditions
from src.calculate import calculate_index,count_value, percent_value, percent_to_text
from src.core import expert_system
from random import randint

class Main(QDialog):
    def __init__(self):
        super(Main,self).__init__()
        loadUi("src/frontend/main.ui",self)
        self.crawlBtn.clicked.connect(self.loadCrawlDataFunction)
        self.advisoryBtn.clicked.connect(self.advisoryFunction)
        self.addRuleBtn.clicked.connect(self.addRuleFunction)
        self.updateBtn.clicked.connect(self.updateRuleFunction)
        self.reloadBtn.clicked.connect(self.reloadRuleFunction)
        self.deleteBtn.clicked.connect(self.deleteRuleFunction)
        self.loadRule()
        self.ruleTbl.clicked.connect(self.getItemFunction)
        self.calculated_data = None
        self.mainwindow = None 
        self.secondwindow = None

    def loadRule(self):
        print('load rule')
        docs = find_all_rules()
        self.ruleTbl.setRowCount(len(docs))
        self.ruleTbl.setColumnWidth(0, 250)
        self.ruleTbl.setColumnWidth(1, 100)
        self.ruleTbl.setColumnWidth(2, 100)
        self.ruleTbl.setColumnWidth(3, 100)
        self.ruleTbl.setColumnWidth(4, 236)

        i = 0
        conditionStr = ''
        for doc in docs:
            print(doc["_id"])
            self.ruleTbl.setItem(i, 0, QtWidgets.QTableWidgetItem(doc["_id"]))
            self.ruleTbl.setItem(i, 1, QtWidgets.QTableWidgetItem(doc["name"]))
            self.ruleTbl.setItem(i, 2, QtWidgets.QTableWidgetItem(doc["description"]))
            self.ruleTbl.setItem(i, 3, QtWidgets.QTableWidgetItem(doc["value"]))
            print(doc["conditions"])
            for condition in doc["conditions"]:
                conditionStr = condition[0] + ' ' +  condition[1] + ' ' + condition[2] + '\n'
            self.ruleTbl.setItem(i, 4, QtWidgets.QTableWidgetItem(conditionStr))
            i+= 1
        print(docs)
    
    def getItemFunction(self):
        print('get item')
        row = self.ruleTbl.currentRow()
        col = self.ruleTbl.currentColumn()
        # text = self.ruleTbl.item(row, col).text()

        rowItemId = self.ruleTbl.item(row,0).text()
        rowItemName= self.ruleTbl.item(row,1).text()
        rowItemDes= self.ruleTbl.item(row,2).text()
        rowItemValue= self.ruleTbl.item(row,3).text()
        rowItemCondition= self.ruleTbl.item(row,4).text()
        return rowItemId,rowItemName,rowItemDes,rowItemValue,rowItemCondition

    def get_calculated_data(self):
        data = solve(self.stockInput.text())
        self.calculated_data = data
        return calculate_index(data)

    def loadCrawlDataFunction(self):
        calculated_data = self.get_calculated_data()

        self.dataTbl.setRowCount(len(calculated_data))
        self.dataTbl.setColumnWidth(0, 300)
        self.dataTbl.setColumnWidth(1, 175)

        index = 0
        for field, value in calculated_data.items():
            self.dataTbl.setItem(index, 0, QtWidgets.QTableWidgetItem(field))
            self.dataTbl.setItem(index, 1, QtWidgets.QTableWidgetItem(str(value)))
            index += 1


    def advisoryFunction(self):
        self.resultLb.setAlignment(Qt.AlignCenter)
        data = self.calculated_data
        if not data:
            self.resultLb.setText("Chưa có dữ liệu để tư vấn")
            return
        rules = find_all_rules()
        if not rules:
            self.resultLb.setText("Chưa có đủ luật để tư vấn")
            return
        point = expert_system(rules, data)
        total_point_rule = count_value(rules)
        percent = percent_value(point, total_point_rule)
        result = percent_to_text(percent, point, total_point_rule)
        self.resultLb.setText(result)

    def addRuleFunction(self):
        print('open window create rule')
        if self.secondwindow is None:
            self.secondwindow = CreateRule()
        self.secondwindow.show()  

    def updateRuleFunction(self):
        print('update')
        rowItemId,rowItemName,rowItemDes,rowItemValue,rowItemCondition = self.getItemFunction()
        update_new_rule(rowItemId,rowItemName,rowItemDes,rowItemValue,rowItemCondition)
        self.loadRule()

    def deleteRuleFunction(self, checked):
        print('open window delete rule')
        if self.mainwindow is None:
            self.mainwindow = DeleteRule()
        self.mainwindow.show()

    def reloadRuleFunction(self):
        print('reload rule')
        self.loadRule()

class CreateRule(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Nhập thông tin:" )
        self.setFixedHeight(850)
        self.setFixedWidth(1000)
        self.setWindowTitle("Nhập tập luât")
        layout.addWidget(self.label)

        self.nameLb = QLabel("Nhập tên tập luật")
        self.nameInput = QLineEdit(self)
        self.nameInput.move(20, 20)
        self.nameInput.resize(280,40)

        self.desLb = QLabel("Nhập mô tả tập luật")
        self.descriptionInput = QLineEdit(self)
        self.descriptionInput.move(20, 20)
        self.descriptionInput.resize(280,40)

        self.valueLb = QLabel("Nhập giá tri tập luật")
        self.valueInput = QLineEdit(self)
        self.valueInput.move(20, 20)
        self.valueInput.resize(280,40)

        self.ruleLb = QLabel("Nhập tập luật")
        self.ruleInput = QPlainTextEdit(self)
        self.ruleInput.move(45, 235)
        self.ruleInput.resize(500,250)

        layout.addWidget(self.nameLb)
        layout.addWidget(self.nameInput)
        layout.addWidget(self.desLb)
        layout.addWidget(self.descriptionInput)
        layout.addWidget(self.valueLb)
        layout.addWidget(self.valueInput)
        layout.addWidget(self.ruleLb)
        layout.addWidget(self.ruleInput)

        self.infoLb = QLabel("Gợi ý các điều kiện của tập luật:\nEPS\nLNST\nROE\nEPS_rating\nAD_rating\nRS_rating\nSMR_rating\n....")
        layout.addWidget(self.infoLb)

        self.tableWidget = QTableWidget()
        self.loadRule()
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)

        self.button = QPushButton("Create rule", self)
 
        # adding action to a button
        self.button.clicked.connect(self.createRule)
 
        # accessing the name of button
        self.name = self.button.accessibleName()
 
        # creating a label to display a name
        self.label1 = QLabel(self)
        self.label1.setText(self.name)
        self.label1.move(200, 200)

        layout.addWidget(self.tableWidget)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def loadRule(self):
        print('load rule in delete popup')
        docs = find_all_rules()
        self.tableWidget.setRowCount(len(docs))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Tên", "Mô tả", "Giá trị", "Điều kiện"])
        print(len(docs))
        conditionStr = ''
        index = 0
        for doc in docs:
            self.tableWidget.setItem(index, 0, QtWidgets.QTableWidgetItem(doc["_id"]))
            self.tableWidget.setItem(index, 1, QtWidgets.QTableWidgetItem(doc["name"]))
            self.tableWidget.setItem(index, 2, QtWidgets.QTableWidgetItem(doc["description"]))
            self.tableWidget.setItem(index, 3, QtWidgets.QTableWidgetItem(doc["value"]))
            for condition in doc["conditions"]:
                conditionStr = condition[0] + ' ' +  condition[1] + ' ' + condition[2] + '\n'
            self.tableWidget.setItem(index, 4, QtWidgets.QTableWidgetItem(conditionStr))    
            index += 1

    def getItemFunction(self):
        print('get item')
        row = self.tableWidget.currentRow()
        col = self.tableWidget.currentColumn()
        rowItemId = self.tableWidget.item(row,0).text()
        rowItemName= self.tableWidget.item(row,1).text()
        rowItemDes= self.tableWidget.item(row,2).text()
        rowItemValue= self.tableWidget.item(row,3).text()
        rowItemCondition= self.tableWidget.item(row,4).text()
        return rowItemId,rowItemName,rowItemDes,rowItemValue,rowItemCondition

    def createRule(self):
        print('createRule')
        try:
            rule_new = insert_new_rule(self.nameInput.text(), self.descriptionInput.text(), self.valueInput.text(), self.ruleInput.toPlainText())
            self.nameInput.clear()
            self.descriptionInput.clear()
            self.valueInput.clear()
            self.ruleInput.clear()
            self.loadRule()
        except:
            print('failed')

class DeleteRule(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Xóa tập luât")
        layout = QVBoxLayout()
        self.label = QLabel("Chọn dòng muốn xóa:" )
        self.setFixedHeight(500)
        self.setFixedWidth(1000)
        layout.addWidget(self.label)

        self.tableWidget = QTableWidget()
        self.loadRule()
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)

        self.button = QPushButton("Delete rule", self)
 
        # setting name
        self.button.setAccessibleName("push button")
 
        # adding action to a button
        self.button.clicked.connect(self.deleteRule)
 
        # accessing the name of button
        self.name = self.button.accessibleName()
 
        # creating a label to display a name
        self.label1 = QLabel(self)
        self.label1.setText(self.name)
        self.label1.move(200, 200)

        layout.addWidget(self.tableWidget)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def loadRule(self):
        print('load rule in delete popup')
        docs = find_all_rules()
        self.tableWidget.setRowCount(len(docs))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Tên", "Mô tả", "Giá trị", "Điều kiện"])
        print(len(docs))
        conditionStr = ''
        index = 0
        for doc in docs:
            self.tableWidget.setItem(index, 0, QtWidgets.QTableWidgetItem(doc["_id"]))
            self.tableWidget.setItem(index, 1, QtWidgets.QTableWidgetItem(doc["name"]))
            self.tableWidget.setItem(index, 2, QtWidgets.QTableWidgetItem(doc["description"]))
            self.tableWidget.setItem(index, 3, QtWidgets.QTableWidgetItem(doc["value"]))
            for condition in doc["conditions"]:
                conditionStr = condition[0] + ' ' +  condition[1] + ' ' + condition[2] + '\n'
            self.tableWidget.setItem(index, 4, QtWidgets.QTableWidgetItem(conditionStr))    
            index += 1

    def getItemFunction(self):
        print('get item')
        row = self.tableWidget.currentRow()
        col = self.tableWidget.currentColumn()
        rowItemId = self.tableWidget.item(row,0).text()
        rowItemName= self.tableWidget.item(row,1).text()
        rowItemDes= self.tableWidget.item(row,2).text()
        rowItemValue= self.tableWidget.item(row,3).text()
        rowItemCondition= self.tableWidget.item(row,4).text()
        return rowItemId,rowItemName,rowItemDes,rowItemValue,rowItemCondition

    def deleteRule(self):
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

app=QApplication(sys.argv)
mainwindow=Main()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1400)
widget.setFixedHeight(810)
widget.setWindowTitle("Dự đoán cổ phiếu")
widget.show()
app.exec_()