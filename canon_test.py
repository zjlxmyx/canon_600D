import sys
import numpy as np
import CanonLib
from ui_canon_test import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from turbojpeg import TurboJPEG
import time

jpeg = TurboJPEG("turbojpeg.dll")


class GUIMainWindow(Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.init_UI()
        self.camera_thread = CameraThread()
        self.camera_thread.CameraSignal.connect(self.camera_show)
        self.pushButton_camera.setText('Camera')

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
        # self.camera_thread.flag = False
        self.camera_thread.camera.set_Capture_ready()
        self.camera_thread.camera.get_Capture_image()
        # self.camera_thread.flag = True
        # self.camera_thread.start()

    def camera_show(self, image):
        frame = jpeg.decode(image)
        Qimg = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        Qimg = Qimg.rgbSwapped()
        pixmap = QtGui.QPixmap.fromImage(Qimg)

        self.label_image_show.setPixmap(pixmap)


class CameraThread(QtCore.QThread):
    CameraSignal = QtCore.pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.camera = CanonLib.CanonCamera()
        self.camera.Init_Camera()
        self.data = None
        self.flag = None

    def run(self):
        self.camera.set_LiveView_ready()
        while self.flag:
            self.data = self.camera.get_Live_image()
            if (self.data.size != 0) and (self.data[0] != 0):
                self.CameraSignal.emit(self.data)
                time.sleep(0.1)
        self.camera.Release_Live()








if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = GUIMainWindow()
    sys.exit(app.exec_())
