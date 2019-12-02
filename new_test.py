import CanonLib
from turbojpeg import TurboJPEG
jpeg = TurboJPEG("C:\\turbojpeg.dll")
import cv2

c = CanonLib.CanonCamera()
c.Init_Camera()
c.set_LiveView_ready()
while True:
    data = c.get_Live_image()
    if (data.size != 0) and (data[0] != 0):

        frame = jpeg.decode(data)
        # frame = numpy.reshape(data, (3456, 5184, 3))
        # # frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        cv2.imshow("SimpleLive_Python_uEye_OpenCV", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

c.Terminate()
