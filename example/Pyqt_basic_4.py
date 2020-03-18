import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pyqt_basic_ui import Ui_MainWindow


# from_class=uic.loadUiType('D:/mini_pro/example/basictest_1.ui')[0]

class TestForm(QMainWindow, Ui_MainWindow): #PyQt5.QtWidgets에서 상속됨
    #생성자
    def __init__(self):
        super().__init__() #부모의 생성자 호출
        self.setupUi(self) # 함수 선언



if __name__ == "__main__":     # 클래스 전체 호출
    app=QApplication(sys.argv)
    window=TestForm()
    window.show()
    app.exec_()
