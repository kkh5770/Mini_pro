import sys
from PyQt5.QtWidgets import *

app=QApplication(sys.argv) # 현재 위치의 경로를 찾아준다.
#print(sys.argv)  # 파일의 경로

label=QLabel("PyQT First Test!")
label.show() #app를 실행하지 않아서 보이지 않음

print("Before Loop")
app.exec_()
print("After Loop")
