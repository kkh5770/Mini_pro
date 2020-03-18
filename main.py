import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot,pyqtSignal,QUrl
from PyQt5 import uic
from lib.YouViewLayout import Ui_MainWindow
from lib.AuthDialog import AuthDialog
from PyQt5 import QtWebEngineWidgets
import re
import datetime
import sys
import io
from pytube import YouTube
import pytube

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

#from_class=uic.loadUiType('D:/mini_pro/ui/basic_mhp.ui')[0]

class Main(QMainWindow, Ui_MainWindow): #PyQt5.QtWidgets에서 상속됨
    #생성자
    def __init__(self):
        super().__init__() #부모의 생성자 호출
        #초기화
        self.setupUi(self) # 함수 선언
        #인증버튼 이벤트 후
        self.initAuthUnlock()
        #인증버튼 이벤트 전
        self.initAuthLock()
        #setupUI
        #시그널 초기화
        self.initSignal()

        #로그인 관련 변수 선언(로그인 정보를 담을 변수)
        self.user_id=None
        self.user_pw=None
        #재생 여부
        self.is_play=False
        #youtube 관련 변수 선언
        self.youtb=None
        self.youtb_fsize=0

    #기본 UI 비활성화
    def initAuthLock(self):
        self.previewButton.setEnabled(False)
        self.fileNavButton.setEnabled(False)
        self.streamComboBox.setEnabled(False)
        self.startButton.setEnabled(False)
        self.calendarWidget.setEnabled(False)
        self.urlTextEdit.setEnabled(False)
        self.pathTextEdit.setEnabled(False)
        self.showStatusMsg('인증안됨')


    def initAuthUnlock(self):
        self.previewButton.setEnabled(True)
        self.fileNavButton.setEnabled(True)
        self.streamComboBox.setEnabled(True)
        self.startButton.setEnabled(True)
        self.calendarWidget.setEnabled(True)
        self.urlTextEdit.setEnabled(True)
        self.pathTextEdit.setEnabled(True)
        self.showStatusMsg('인증완료')

    def showStatusMsg(self,msg):
        self.statusbar.showMessage(msg)

    #시그널 초기화
    def initSignal(self):
        self.loginButton.clicked.connect(self.authCheck)
        self.previewButton.clicked.connect(self.load_url)
        self.exitButton.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.webEngineView.loadProgress.connect(self.showProgressBrowerLoading)
        self.fileNavButton.clicked.connect(self.selectDownPath)
        self.calendarWidget.clicked.connect(self.append_date)
        self.startButton.clicked.connect(self.downloadYoutb)

    @pyqtSlot() #명시적 표현(유지보수 때문에 슬롯과 시그널이 여러개일 때 시그널은 시그널끼리 슬롯은 슬롯끼리 모아 놓는 책깔피 개념)
    def authCheck(self):
        #print('test')
        dlg=AuthDialog()
        dlg.exec_()
        self.user_id=dlg.user_id
        self.user_pw=dlg.user_pw
        #print("id : %s Password : %s" %(self.user_id,self.user_pw))
        #이 부분에서 필요한 경우 실제 로컬 DB 또는 서버 연동 후
        # 유저 정보 및 사용자 유효기간을 체크하는 코딩

        if True: #강제로 아이디 비번 모두 인증완료
            self.initAuthUnlock()#로그인후 모두 비활성화
            self.loginButton.setText("인증완료")
            self.loginButton.setEnabled(False) #로그인버튼 비활성화
            self.urlTextEdit.setFocus(True) #커서이동
            self.append_log_msg("login Success")
        else:
            QMessageBox.about(self, "인증오류","아이디 또는 비밀번호가 맞지 않습니다.")

    def load_url(self):
        url = self.urlTextEdit.text().strip()
        v = re.compile('^https://www.youtube.com/?')
        if self.is_play : # 재생중일 때 멈춤
            self.append_log_msg('Stop Click')
            self.webEngineView.load(QUrl('about:blank')) #about:blank:빈페이지로 초기화
            self.previewButton.setText('Play')
            self.is_play=False
            self.urlTextEdit.clear()
            self.urlTextEdit.setFocus(True)
            self.startButton.setEnabled(False)
            self.streamComboBox.clear() #저장 완료시 초기화
            self.progressBar_2.setValue(0) #다운로드 완료시 초기화
            self.showStatusMsg("인증완료")

        else : #play 되지 않은 상태
            if v.match(url) is not None :
                self.append_log_msg('Play Click')
                self.webEngineView.load(QUrl(url))
                #상태표시줄
                self.showStatusMsg(url + "재생중")
                self.previewButton.setText("Stop")
                self.is_play=True
                self.startButton.setEnabled(True)
                self.initialYouWork(url)
            else:
                QMessageBox.about(self,"URL 형식오류","Youtube 주소 형식이 아닙니다")
                self.urlTextEdit.clear()
                self.urlTextEdit.setFocus(True)

    def initialYouWork(self,url):
        video_list=pytube.YouTube(url)
        #로딩바 계산
        video_list.register_on_progress_callback(self.showProgressDownload)
        self.youtb=video_list.streams.all()
        self.streamComboBox.clear()
        for q in self.youtb:
            #print(q)
            tmp_list,str_list=[],[]
            tmp_list.append(str(q.mime_type or ''))
            tmp_list.append(str(q.resolution or ''))
            tmp_list.append(str(q.fps or ''))
            tmp_list.append(str(q.abr or ''))

            str_list=[x for x in tmp_list if x!='']
            print('join',','.join(str_list))
            self.streamComboBox.addItem(','.join(str_list))


    def append_log_msg(self,act): #act:login Success
        now=datetime.datetime.now()
        nowDatetime=now.strftime('%Y-%m-%d %H:%M:%S')
        app_msg=self.user_id +' : '+ act + " - ("+ nowDatetime +")"
        print(app_msg)
        self.plainTextEdit.appendPlainText(app_msg)

        #활동 로그 저장(서버 DB를 사용)
        with open('D:/mini_pro/log/log.text','a')as f:
            f.write(app_msg+'\n')


    @pyqtSlot(int)
    def showProgressBrowerLoading(self,v):
        self.loadProgress.setValue(v)

    def selectDownPath(self):
        print('test')
        #파일선택
        # fname=QFileDialog.getOpenFileName(self)
        # self.pathTextEdit.setText(fname[0])

        #경로 선택
        fpath=QFileDialog.getExistingDirectory(self,'select Directory')
        self.pathTextEdit.setText(fpath)


    def append_date(self):
        cur_date = self.calendarWidget.selectedDate()
        print(str(cur_date.year())+'-'+str(cur_date.month())+'-'+str(cur_date.day()))
        self.append_log_msg("Calendar Click")

    # @pyqtSlot()
    def downloadYoutb(self):
        down_dir=self.pathTextEdit.text().strip()
        if down_dir is None or down_dir=='' or not down_dir:
            QMessageBox.about(self,"경로선택","다운로드 받을 경로를 다시 선택하세요")
            return None
        self.youtb_fsize=self.youtb[self.streamComboBox.currentIndex()].filesize
        print('fsize: ',self.youtb_fsize)
        self.youtb[self.streamComboBox.currentIndex()].download(down_dir)
        self.append_log_msg('Download click')

    def showProgressDownload(self, chunk, file_handler, bytes_remaining):
        # print(int(self.youtb_fsize - bytes_remaining))
        print('bytes_remaining',bytes_remaining)
        self.progressBar_2.setValue(int(((self.youtb_fsize - bytes_remaining) / self.youtb_fsize) * 100))


if __name__ == "__main__":     # 클래스 전체 호출
    app=QApplication(sys.argv)
    you_viewer_main=Main()
    you_viewer_main.show()
    app.exec_()
