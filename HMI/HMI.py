import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
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
        self.replied_time = QTimer()
        self.replied_time.setInterval(20000)
        self.wav_in = 'in.mp3'
        check_response_ui = 'check.ui'
        uic.loadUi(check_response_ui, self)
        self.setWindowTitle('알림')

        if self.parent.re == 1:
            self.btn_re.setText(f'{parent.btn_1.text()}')
            self.btn_re.setStyleSheet("color: black;"
                                     "border-style: solid;"
                                     "border-width: 3px;"
                                     "background-color: #fa8d87;"
                                     "border-color: #f7453b;"
                                     "border-radius: 3px")
        elif self.parent.re == 2:
            self.btn_re.setText(f'{parent.btn_2.text()}')
            self.btn_re.setStyleSheet("color: black;"
                                     "border-style: solid;"
                                     "border-width: 3px;"
                                     "background-color: #fcdcae;"
                                     "border-color: #f79914;"
                                     "border-radius: 3px")
        elif self.parent.re == 3:
            self.btn_re.setText(f'{parent.btn_3.text()}')
            self.btn_re.setStyleSheet("color: black;"
                                     "border-style: solid;"
                                     "border-width: 3px;"
                                     "background-color: #87CEFA;"
                                     "border-color: #4a7ac2;"
                                     "border-radius: 3px")
        else:
            self.btn_re.setText(f'{parent.btn_4.text()}')
            self.btn_re.setStyleSheet("color: black;"
                                     "border-style: solid;"
                                     "border-width: 3px;"
                                     "background-color: #ebf0c0;"
                                     "border-color: #c4d900;"
                                     "border-radius: 3px")

        self.btn_re.setFont(QFont("Gulim",40))
        self.lbl_re.setStyleSheet("color: red;"
                                 "border-style: solid;"
                                 "border-width: 2px;"
                                 "background-color: #fcbdbd;"
                                 "border-color: #FA8072;"
                                 "border-radius: 3px")

        self.show()

        self.clicked_time.timeout.connect(self.record_csv)
        self.replied_time.timeout.connect(self.replied)
        self.btn_re.clicked.connect(self.btn)

        self.clicked_time.start()
        self.replied_time.start()

    def btn(self):
        self.clicked_time.stop()
        self.replied_time.stop()
        self.close()
        playsound(self.wav_in)
        self.parent.show()
        self.parent.remind_time.start()
        self.parent.record_time.start()

    def record_csv(self):
        self.clicked_time.stop()
        raw_data = [(time.time(), self.parent.name, self.parent.re)]
        data = pd.DataFrame(raw_data, columns=self.parent.df.columns)
        self.parent.df = self.parent.df.append(data)
        self.parent.df.to_csv(f'{self.parent.name}.csv', index=False, encoding='utf-8-sig')
        self.hide()

    def show_parent(self):
        self.parent.remind_time.start()
        self.parent.record_time.start()
        self.parent.show()

    def replied(self):
        self.replied_time.stop()
        playsound(self.wav_in)
        self.show_parent()

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.name = '류정환' #driver_name으로 교체
        self.re = 0
        self.wav_out = 'out.mp3'###
        self.wav_in = 'in.mp3'###
        self.filename = self.name + '.csv'

        self.remind_time = QTimer()
        self.remind_time.setInterval(5000)
        self.record_time = QTimer()
        self.record_time.setInterval(10000)
        self.reshow_time = QTimer()
        self.reshow_time.setInterval(10000)

        if os.path.exists(self.filename):
            print(f'{self.name} 기록 시작합니다')
        else:
            df = pd.DataFrame(columns=['time', 'driver', 'status'])
            df.to_csv(self.filename, index=False)
            print(f'{self.filename} 파일을 생성하였습니다')
        self.df = pd.read_csv(f'{self.name}.csv', encoding='utf-8-sig')
        self.setWindowTitle('기록중')

        pal = QPalette()
        pal.setColor(QPalette.Background,QColor(255,255,255))
        self.lbl_driver.setFont(QFont("Gulim",40))
        self.setPalette(pal)

        self.setWindowModality(2)
        self.show()
        self.lbl_driver.setText(self.name)
        pixmap = QPixmap('캡처.png')
        self.lbl_image.setPixmap(QPixmap(pixmap))
        self.btn_1.clicked.connect(self.btn1)
        self.btn_2.clicked.connect(self.btn2)
        self.btn_3.clicked.connect(self.btn3)
        self.btn_4.clicked.connect(self.btn4)

        self.lbl_driver.setStyleSheet("color: black;"
                                      "border-style: solid;"
                                      "border-width: 3px;"
                                      "background-color: #87CEFA;"
                                      "border-color: #1E90FF;"
                                      "border-radius: 3px")
        self.btn_1.setStyleSheet("color: black;"
                                 "border-style: solid;"
                                 "border-width: 3px;"
                                 "background-color: #fa8d87;"
                                 "border-color: #f7453b;"
                                 "border-radius: 3px")
        self.btn_2.setStyleSheet("color: black;"
                                 "border-style: solid;"
                                 "border-width: 3px;"
                                 "background-color: #fcdcae;"
                                 "border-color: #f79914;"
                                 "border-radius: 3px")
        self.btn_3.setStyleSheet("color: black;"
                                 "border-style: solid;"
                                 "border-width: 3px;"
                                 "background-color: #87CEFA;"
                                 "border-color: #4a7ac2;"
                                 "border-radius: 3px")
        self.btn_4.setStyleSheet("color: black;"
                                 "border-style: solid;"
                                 "border-width: 3px;"
                                 "background-color: #ebf0c0;"
                                 "border-color: #c4d900;"
                                 "border-radius: 3px")
        playsound(self.wav_in)

        self.remind_time.timeout.connect(self.remind)
        self.record_time.timeout.connect(self.record)
        self.reshow_time.timeout.connect(self.reshow)
        self.remind_time.start()
        self.record_time.start()
        print(self.re)

    def btn1(self):
        self.remind_time.stop()
        self.record_time.stop()
        self.re = 1
        self.hide()
        #os.system(self.wav_out)
        playsound(self.wav_out)
        check_response(self)

    def btn2(self):
        self.remind_time.stop()
        self.record_time.stop()
        self.re = 2
        self.hide()
        #os.system(self.wav_out)
        playsound(self.wav_out)
        check_response(self)

    def btn3(self):
        self.remind_time.stop()
        self.record_time.stop()
        self.re = 3
        self.hide()
        #os.system(self.wav_out)
        playsound(self.wav_out)
        check_response(self)

    def btn4(self):
        self.remind_time.stop()
        self.record_time.stop()
        self.re = 4
        self.hide()
        #os.system(self.wav_out)
        playsound(self.wav_out)
        check_response(self)

    def remind(self):
        self.remind_time.stop()
        playsound(self.wav_in)

    def record(self):
        self.record_time.stop()
        self.reshow_time.start()
        raw_data = [(time.time(), self.name, 0)]
        data = pd.DataFrame(raw_data, columns=self.df.columns)
        self.df = self.df.append(data)
        self.df.to_csv(f'{self.name}.csv', index=False, encoding='utf-8-sig')
        self.hide()

    def reshow(self):
        self.reshow_time.stop()
        self.remind_time.start()
        self.record_time.start()
        playsound(self.wav_in)
        self.show()
    # def keyPressEvent(self, e):
    #     if Qt.key_Enter == true:
    #         QCoreApplication.instance().quit->종료 시그널

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()