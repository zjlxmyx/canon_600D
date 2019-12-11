import sys
import numpy as np
import CanonLib
from ui_canon_test import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import time
from turbojpeg import TurboJPEG
jpeg = TurboJPEG("turbojpeg.dll")


class GUIMainWindow(Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.init_UI()


        self.pushButton_camera.setText('Camera')

        # self.camera = CanonLib.CanonCamera()
        # self.camera.Init_Camera()
        global c
        c = CanonLib.CanonCamera()
        c.Init_Camera()

        self.camera_thread = CameraThread()
        self.camera_thread.CameraSignal.connect(self.camera_show)

    def init_UI(self):
        self.pushButton_camera.clicked.connect(self.camera_task)
        self.pushButton_capture.clicked.connect(self.camera_capture)

    def camera_task(self):
        if self.pushButton_camera.isChecked():
            self.pushButton_camera.setText('Camera ON')
            self.camera_thread.flag = True
            self.camera_thread.start()

        else:
            self.pushButton_camera.setText('Camera')
            self.camera_thread.flag = False

    def camera_capture(self):
        self.camera_thread.flag = False
        time.sleep(1)
        c.set_Capture_ready()
        c.get_Capture_image()
        time.sleep(1)
        self.camera_thread.flag = True
        self.camera_thread.start()

    def camera_show(self, image):
        frame = jpeg.decode(image)
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        Qimg = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        Qimg = Qimg.rgbSwapped()
        pixmap = QtGui.QPixmap.fromImage(Qimg)
        self.label_image_show.setPixmap(pixmap)

        grad_x = cv2.Sobel(frame, -1, 1, 0, ksize=5)
        grad_y = cv2.Sobel(frame, -1, 0, 1, ksize=5)
        grad = cv2.addWeighted(grad_x, 0.5, grad_y, 0.5, 0)
        Qimg = QtGui.QImage(grad.data, grad.shape[1], grad.shape[0], QtGui.QImage.Format_Grayscale8)
        pixmap = QtGui.QPixmap.fromImage(Qimg)
        self.label_image_show_2.setPixmap(pixmap)
        self.pushButton_capture.setText(str(grad.var()))


    def closeEvent(self, event):
        # global c
        self.camera_thread.quit()
        c.Terminate()


class CameraThread(QtCore.QThread):
    CameraSignal = QtCore.pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.camera = c
        self.data = None
        self.flag = None

        # self.camera = CanonLib.CanonCamera()
        # self.camera.Init_Camera()

    def run(self):

        self.camera.set_LiveView_ready()
        while self.flag:
            self.data = self.camera.get_Live_image()
            if (self.data.size != 0) and (self.data[0] != 0):
                self.CameraSignal.emit(self.data)
                time.sleep(0.1)
        self.camera.Release_Live()
        # self.camera.Terminate()









if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = GUIMainWindow()
    sys.exit(app.exec_())
