# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QLabel,QMainWindow,QFileDialog,QDialog,QPushButton
import pickle
import struct
import copy
postName=".ys"

class node():
    def __init__(self,value=-1,freq=0,father=None):
        self.value=value
        self.freq=freq
        self.father=father
        self.code=""
def WordCounting(words):
    wordset={}
    lis=[]
    for word in words:
        if word in wordset:
            wordset[word]=wordset[word]+1
        else:
            wordset[word]=1
    for key,value in wordset.items():
        temp=node(value=key,freq=value)
        lis.append(temp)
    return lis
def readFile(path):
    file=open(path,'rb')
    data=file.read()
    data=data.decode("utf-8")
    file.close()
    return data
def encodeList(data):
    lis={}
    completed=[]
    todo=data
    while len(todo)!=1:
        todo=sorted(todo,key=lambda k:k.freq,reverse=True)
        a=todo.pop()
        b=todo.pop()
        a.code=a.code+"0" if a.freq<=b.freq else "1"
        b.code = b.code + "0" if a.freq > b.freq else "1"
        completed.append(a)
        completed.append(b)
        father=node(freq=a.freq+b.freq)
        a.father=father
        b.father=father
        todo.append(father)
    completed.append(todo.pop())
    completed.reverse()
    minlen=100
    maxlen=0
    for n in completed:
        if n.father != None:
            n.code =n.code+n.father.code
        if n.value!=-1:
            lis[n.value]=n.code[::-1]
            minlen=min(len(lis[n.value]),minlen)
            maxlen = max(len(lis[n.value]), maxlen)
    return lis,[minlen,maxlen]
def Encode(data,encodelist):
    new=""
    for d in data:
        new=new+encodelist[d]
    return new
def SaveZip(zip,path):
    code=[]
    num=0
    while True:
        temp=hex(int(zip[num:num+8],2))
        num=num+8
        code.append(temp)
        if len(zip)-num<8:
            break
            temp = hex(int(zip[num:], 2))
            code.append(temp)
            break

    # print(code)
    with open(path, "wb") as f:
        for li in code:
            s = struct.pack('B',int(li,16))
            f.write(s)
        f.close()
def Decode(encodelist,data,ra):
    minlen, maxlen=ra[0],ra[1]
    code=copy.copy(data)
    code=code.hex()
    s=str(bin(int(code,16)))
    s=s[2:]
    index=0
    text=""
    while True:
        for i in range(minlen,maxlen+1):
            temp=s[index:index+i]
            if temp in encodelist.keys():
                text=text+encodelist[temp]
                index=i+index
                break
        if index>=len(data):
            break
    return text
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(366, 391)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(60, 150, 240, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(90, 50, 201, 61))
        font = QtGui.QFont()
        font.setFamily("华文行楷")
        font.setPointSize(30)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(50, 200, 271, 131))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.decode = QtWidgets.QPushButton(self.widget)
        self.decode.setObjectName("decode")
        self.verticalLayout.addWidget(self.decode)
        self.encode = QtWidgets.QPushButton(self.widget)
        self.encode.setObjectName("encode")
        self.verticalLayout.addWidget(self.encode)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 366, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "文件压缩工具"))
        self.label.setText(_translate("MainWindow", "文件压缩"))
        self.decode.setText(_translate("MainWindow", "Decode"))
        self.encode.setText(_translate("MainWindow", "Encode"))
class ys(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(ys, self).__init__()
        self.setupUi(self)
        self.connecter()
        self.show()
    def connecter(self):
        self.encode.clicked.connect(self.startEncode)
        self.decode.clicked.connect(self.startDecode)
        # self.path.clicked.connect(self.loadPath)
    def loadPath(self):
        openPath, _ = QFileDialog.getOpenFileName()
        self.lineEdit.setText(openPath)
        return openPath
    def startEncode(self):
        path=self.loadPath()
        data =readFile(path)
        self.encodelist,self.ra=encodeList(WordCounting(data))
        zi =Encode(data,self.encodelist)
        path = "temp" +postName
        SaveZip(zi, path)
        self.label.setText("压缩完成！")
    def startDecode(self):
        path = self.loadPath()
        print(path[-3:])
        if path[-3:] == ".ys":
            with open(path, 'rb') as file:
                data = file.read()
            encodelist = dict(zip(self.encodelist.values(), self.encodelist.keys()))
            print(Decode(data, encodelist, [self.ra[0], self.ra[1]]))
            self.label.setText("解压完成")
        else:
            dialog=QDialog()
            lb=QLabel("文件格式错误",dialog)
            lb.move(50,50)
            dialog.setWindowTitle("提示窗口")
            dialog.setWindowModality(Qt.ApplicationModal)
            dialog.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win=ys()
    win.show()
    sys.exit(app.exec_())