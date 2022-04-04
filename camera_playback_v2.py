import sys
import cv2 as cv
from PyQt5.QtWidgets import *
import ipaddress
import webbrowser

class Play_Cam(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(400, 400)
        self.setWindowTitle("play_rtsp_cam")

        self.all_btn_in_window()
        self.all_lable()
        self.all_input()
        self.rad_btn()

    def open_ie(self):
        if self.ip_add_cum_find(self.input_ip.text()):
            webbrowser.open(self.input_ip.text())
        else:
            self.infobox_ip()

    def rad_btn(self):

        self.chk_enter_sunell = QRadioButton("Sunell", self)
        self.chk_enter_sunell.move(250, 100)
        self.chk_enter_sunell.clicked.connect(self.show_cams_stream)

        self.chk_enter_unv = QRadioButton("UNV", self)
        self.chk_enter_unv.move(250, 120)
        self.chk_enter_unv.clicked.connect(self.show_cams_stream)

        self.chk_enter_dynacolor = QRadioButton("Dynacolor", self)
        self.chk_enter_dynacolor.move(250, 140)
        self.chk_enter_dynacolor.clicked.connect(self.hide_dynacolor_stream)

    def btn_play(self):

        state_btn_sunell = self.chk_enter_sunell.isChecked()
        state_btn_unv = self.chk_enter_unv.isChecked()
        state_btn_dynacolor =self.chk_enter_dynacolor.isChecked()
        ip_address_fnd = self.input_ip.text()
        param_stream_cam = self.input_stream_number.text()
        if state_btn_sunell:
            if self.ip_add_cum_find(ip_address_fnd) != True:
                self.infobox_ip()
            elif param_stream_cam == "1" or param_stream_cam == "2":
                self.play_cam_sta_sunell()
            else:
                self.infobox_number_stream()
        elif state_btn_unv:
            if self.ip_add_cum_find(ip_address_fnd) != True:
                self.infobox_ip()
            elif param_stream_cam == "1" or param_stream_cam == "2":
                self.play_cam_sta_unv()
            else:
                self.infobox_number_stream()
        elif state_btn_dynacolor:
            if self.ip_add_cum_find(ip_address_fnd) != True:
                self.infobox_ip()
            else:
                self.play_cam_sta_dynacolor()

    def hide_dynacolor_stream(self):
        self.lable_stream.hide()
        self.input_stream_number.hide()

    def show_cams_stream(self):
        self.lable_stream.show()
        self.input_stream_number.show()

    def ip_add_cum_find(self, ip_address):
        try:
            ipaddress.ip_network(ip_address)
            return True
        except ValueError:
            return False

    def infobox_ip(self):
        QMessageBox.warning(self, "Error value IP", " Enter Ip correct address")

    def infobox_number_stream(self):
        QMessageBox.critical(self, "info", "incorrect stream number")

    def all_input(self):

        self.input_ip = QLineEdit("", self)
        self.input_ip.move(0, 80)
        self.input_ip.resize(100, 20)
        self.input_ip.setPlaceholderText("000.000.000.000")

        self.input_login = QLineEdit("", self)
        self.input_login.move(0, 120)
        self.input_login.resize(100, 20)
        self.input_login.setText("Admin")

        self.input_pass = QLineEdit("", self)
        self.input_pass.move(0, 160)
        self.input_pass.resize(100, 20)
        self.input_pass.setText("1234")

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

        self.btn_open_ie = QPushButton("Open IE", self)
        self.btn_open_ie.move(200, 0)
        self.btn_open_ie.clicked.connect(self.open_ie)

        self.btn_show_cam = QPushButton("Play", self)
        self.btn_show_cam.move(0, 0)
        self.btn_show_cam.clicked.connect(self.btn_play)

        self.button_play_cum_exit = QPushButton("Close Cam", self)
        self.button_play_cum_exit.move(100, 0)
        self.button_play_cum_exit.clicked.connect(self.new_close)

    def new_close(self):
        res = QMessageBox.question(self, " Exit ", " Close cam ? ")
        if res == QMessageBox.Yes:
            self.ret_key_q = 113
            self.input_stream_number.setText("")
        elif res == QMessageBox.No:
            QMessageBox.information(self, " info", " Continue")

    def play_cam_sta_unv(self):
        self.ret_key_q = 0
        cap = cv.VideoCapture(f"rtsp://{self.input_login.text()}:{self.input_pass.text()}@{self.input_ip.text()}"
                              f"/media/video{self.input_stream_number.text()}/video")
        while cap.isOpened():
            ret, frame = cap.read()
            # if frame is read correctly ret is True
            if not ret:
                QMessageBox.information(self, "info", "incorrect param")
                break
            rgb_color = cv.cvtColor(frame, cv.COLOR_RGBA2RGB)
            cv.imshow('frame', rgb_color)
            if cv.waitKey(1) == ord("q") or self.ret_key_q == 113:
                break

        cap.release()
        cv.destroyAllWindows()

    def play_cam_sta_sunell(self):
        self.ret_key_q = 0
        cap = cv.VideoCapture(f"rtsp://{self.input_login.text()}:{self.input_pass.text()}@{self.input_ip.text()}"
                              f"/snl/live/1/{self.input_stream_number.text()}/cx/sido=-A0my1A==")
        while cap.isOpened():
            ret, frame = cap.read()
            # if frame is read correctly ret is True
            if not ret:
                QMessageBox.information(self, "info", "incorrect param")
                break
            rgb_color = cv.cvtColor(frame, cv.COLOR_RGBA2RGB)
            cv.imshow('frame', rgb_color)
            if cv.waitKey(1) == ord("q") or self.ret_key_q == 113:
                break

        cap.release()
        cv.destroyAllWindows()

    def play_cam_sta_dynacolor(self):
        self.ret_key_q = 0
        cap = cv.VideoCapture(f"rtsp://{self.input_login.text()}:{self.input_pass.text()}@{self.input_ip.text()}"
                              f":554/h264")
        while cap.isOpened():
            ret, frame = cap.read()
            # if frame is read correctly ret is True
            if not ret:
                QMessageBox.information(self, "info", "incorrect param")
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





