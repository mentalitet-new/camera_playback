import sys
import cv2 as cv
from PyQt5.QtWidgets import *



class Play_Cam(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(400, 400)
        self.setWindowTitle("play_rtsp_cam")

        self.all_btn_in_window()
        self.all_lable()
        self.all_input()

    def all_input(self):

        self.input_ip = QLineEdit("", self)
        self.input_ip.move(0, 80)
        self.input_ip.resize(140, 20)

        self.input_login = QLineEdit("", self)
        self.input_login.move(0, 120)
        self.input_login.resize(100, 20)

        self.input_pass = QLineEdit("", self)
        self.input_pass.move(0, 160)
        self.input_pass.resize(100, 20)

        self.input_stream_number = QLineEdit("", self)
        self.input_stream_number.move(0, 200)
        self.input_stream_number.resize(100, 20)

    def all_lable(self):

        self.lable_ip = QLabel("enter IP cam", self)
        self.lable_ip.move(0, 55)

        self.lable_login = QLabel("enter login cam", self)
        self.lable_login.move(0, 95)

        self.lable_pass = QLabel("enter password cam", self)
        self.lable_pass.move(0, 135)

        self.lable_stream = QLabel("enter Stream number", self)
        self.lable_stream.move(0, 175)

    def all_btn_in_window(self):

        self.button_play_cum = QPushButton("Play", self)
        self.button_play_cum.move(0, 0)
        self.button_play_cum.clicked.connect(self.play_cam_sta)

        self.button_play_cum_exit = QPushButton("Close Cam", self)
        self.button_play_cum_exit.move(100, 0)
        self.button_play_cum_exit.clicked.connect(self.new_close)

    def new_close(self):
        res = QMessageBox.question(self, " Exit ", " Close cam ? ")
        if res == QMessageBox.Yes:
            self.ret_key_q = 113
        elif res == QMessageBox.No:
            QMessageBox.information(self, " info", " Continue")

    def play_cam_sta(self):

        self.ret_key_q = 0
        cap = cv.VideoCapture(f"rtsp://{self.input_login.text()}:{self.input_pass.text()}@{self.input_ip.text()}"
                              f"/snl/live/1/{self.input_stream_number.text()}/cx/sido=-A0my1A==")
        while cap.isOpened():
            ret, frame = cap.read()
            # if frame is read correctly ret is True
            if not ret:
                QMessageBox.information(self, "info", " incorrect param")
                break
            rgb_color = cv.cvtColor(frame, cv.COLOR_RGBA2RGB)
            cv.imshow('frame', rgb_color)
            if cv.waitKey(1) == ord("q") or self.ret_key_q == 113:
                break


        cap.release()
        cv.destroyAllWindows()

if __name__ == "__main__":
    app = QApplication(sys.argv)  # creat application
    dlgMain = Play_Cam()  # create main window
    dlgMain.show()  # show window
    sys.exit(app.exec_())





