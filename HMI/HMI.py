import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from gtts import gTTS
from playsound import playsound
import pandas as pd
import time
import os

form_class = uic.loadUiType("status.ui")[0]

class check_response(QDialog):
    def __init__(self, parent):
        super(check_response, self).__init__(parent)
        self.parent = parent
        self.clicked_time = QTimer()
        self.clicked_time.setInterval(10000)
        self.audio_in = 'in.mp3'

        check_response_ui = 'check.ui'
        uic.loadUi(check_response_ui, self)
        self.setWindowTitle('알림')
        self.btn_re.setText(f'{parent.re}번')
        self.btn_re.setFont(QFont("궁서",50))
        self.lbl_re.setStyleSheet("color: red;"
                                 "border-style: solid;"
                                 "border-width: 2px;"
                                 "background-color: #fcbdbd;"
                                 "border-color: #FA8072;"
                                 "border-radius: 3px")
        self.btn_re.setStyleSheet("color: black;"
                                  "border-style: solid;"
                                  "border-width: 2px;"
                                  "background-color: #c4c4c4;"
                                  "border-color: black;"
                                  "border-radius: 3px")
        self.show()

        self.clicked_time.timeout.connect(self.record_csv)
        self.btn_re.clicked.connect(self.btn)

        self.clicked_time.start()

    def btn(self):
        self.clicked_time.stop()
        #playsound(self.audio_in)
        self.close()
        self.parent.show()

    def record_csv(self):
        self.clicked_time.stop()
        raw_data = [(time.time(), self.parent.name, self.parent.re)]
        data = pd.DataFrame(raw_data, columns=self.parent.df.columns)
        self.parent.df = self.parent.df.append(data)
        self.parent.df.to_csv(f'{self.parent.name}.csv', index=False, encoding='utf-8-sig')
        self.close()
        self.replied()
        self.show_parent()

    def show_parent(self):
        self.parent.show()

    def replied(self):
        time.sleep(20)

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.name = 'test' #driver_name으로 교체
        self.re = 0
        self.audio_out = 'out.mp3'
        self.filename = self.name + '.csv'
        if os.path.exists(self.filename):
            print(f'{self.name} 기록 시작합니다')
        else:
            df = pd.DataFrame(columns=['time', 'driver', 'status'])
            df.to_csv(self.filename, index=False)
            print(f'{self.filename} 파일을 생성하였습니다')
        self.df = pd.read_csv(f'{self.name}.csv', encoding='utf-8-sig')
        self.setWindowTitle('기록중')
        self.setWindowModality(2)
        self.show()
        self.lbl_driver.setText(self.name)
        pixmap = QPixmap('tempsnip.png')
        self.lbl_image.setPixmap(QPixmap(pixmap))
        self.btn_1.clicked.connect(self.btn1)
        self.btn_2.clicked.connect(self.btn2)
        self.btn_3.clicked.connect(self.btn3)

        self.lbl_driver.setStyleSheet("color: black;"
                                      "border-style: solid;"
                                      "border-width: 2px;"
                                      "background-color: #87CEFA;"
                                      "border-color: #1E90FF;"
                                      "border-radius: 3px")
        self.btn_1.setStyleSheet("color: white;"
                                 "border-style: solid;"
                                 "border-width: 2px;"
                                 "background-color: #f7453b;"
                                 "border-color: #f7453b;"
                                 "border-radius: 3px")
        self.btn_2.setStyleSheet("color: white;"
                                 "border-style: solid;"
                                 "border-width: 2px;"
                                 "background-color: #fcc82b;"
                                 "border-color: #fcc82b;"
                                 "border-radius: 3px")
        self.btn_3.setStyleSheet("color: white;"
                                 "border-style: solid;"
                                 "border-width: 2px;"
                                 "background-color: #4a7ac2;"
                                 "border-color: #4a7ac2;"
                                 "border-radius: 3px")

    def btn1(self):
        self.re = 1
        self.hide()
        #playsound(self.audio_out)
        check_response(self)

    def btn2(self):
        self.re = 2
        self.hide()
        #playsound(self.audio_out)
        check_response(self)

    def btn3(self):
        self.re = 3
        self.hide()
        #playsound(self.audio_out)
        check_response(self)

    # def keyPressEvent(self, e):
    #     if Qt.key_Enter == true:
    #         QCoreApplication.instance().quit->종료 시그널

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()