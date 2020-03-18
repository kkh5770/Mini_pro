import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore

class TestForm(QMainWindow): #PyQt5.QtWidgets에서 상속됨
    #생성자
    def __init__(self):
        super().__init__() #부모의 생성자 호출
        self.setupUI() # 함수 선언

    def setupUI(self):
        self.setWindowTitle("PyQT test")
        self.setGeometry(800,400,500,500)

        label_1=QLabel("입력 테스트",self)
        label_2=QLabel("출력 테스트",self)

        label_1.move(20,20)
        label_2.move(20,60)

        self.lineEdit=QLineEdit("",self) # Default 값(글자만 쓸수있다.)
        self.plainEdit=QtWidgets.QPlainTextEdit(self)    # 글자 그림 동영상 편집까지 가능
        self.plainEdit.setReadOnly(True) #쓰기 방지(읽기만 가능)

        self.lineEdit.move(90,20)
        self.plainEdit.setGeometry(QtCore.QRect(20,90,361,231))

        self.lineEdit.textChanged.connect(self.lineEditChanged) # 시그널
        self.lineEdit.returnPressed.connect(self.lineEditEnter)

        #상태바
        self.statusBar=QStatusBar(self)
        self.setStatusBar(self.statusBar)

    def lineEditChanged(self):
        self.statusBar.showMessage(self.lineEdit.text()) # 슬롯

    def lineEditEnter(self):
        self.plainEdit.appendPlainText(self.lineEdit.text())
        self.lineEdit.clear() #메모리 해제


if __name__ == "__main__":     # 클래스 전체 호출
    app=QApplication(sys.argv)
    window=TestForm()
    window.show()
    app.exec_()
