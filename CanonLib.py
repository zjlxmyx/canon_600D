import ctypes
import os
import numpy
import cv2
from turbojpeg import TurboJPEG
import win32gui
import win32api
import win32con
from threading import Timer

os.environ['path'] += ';C:\\Users\\yanxin\\PycharmProjects\\canon_600D'
EDSDK = ctypes.cdll.LoadLibrary('C:\\Users\\yanxin\PycharmProjects\\canon_600D\\EDSDK.dll')
jpeg = TurboJPEG("turbojpeg.dll")


class EdsCapacity(ctypes.Structure):
    _fields_ = [("numberOfFreeClusters", ctypes.c_ulong),
                ("bytesPerSector", ctypes.c_ulong),
                ("reset", ctypes.c_bool)]


class DirectoryItemInfo(ctypes.Structure):
    _fields_ = [("size", ctypes.c_ulonglong),
                ("isFolder", ctypes.c_bool),
                ("groupID", ctypes.c_ulong),
                ("option", ctypes.c_ulong),
                ("szFileName", ctypes.c_char*256),
                ("format", ctypes.c_ulong),
                ("dateTime", ctypes.c_ulong)]


ObjectHandlerType = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)
kEdsObjectEvent_DirItemRequestTransfer = 0x00000208
kEdsFileCreateDisposition_CreateAlways = 1
kEdsAccess_Write = 2
global ImageFilename
ImageFilename = b'C:\\Users\\yanxin\\Desktop\\test.jpg'

def ObjectHandler_py(event, object, context):
    global ImageFilename
    if event == kEdsObjectEvent_DirItemRequestTransfer:
        dirinfo = DirectoryItemInfo()
        Ref = ctypes.c_void_p(object)
        EDSDK.EdsGetDirectoryItemInfo(Ref, ctypes.byref(dirinfo))
        stream = ctypes.c_void_p()
        EDSDK.EdsCreateFileStream(ImageFilename, kEdsFileCreateDisposition_CreateAlways, kEdsAccess_Write, ctypes.byref(stream))
        EDSDK.EdsDownload(Ref, dirinfo.size, stream)
        EDSDK.EdsDownloadComplete(Ref)
        EDSDK.EdsRelease(stream)
ObjectHandler = ObjectHandlerType(ObjectHandler_py)


class CanonCamera:

    def __init__(self):
        self.CameraRef = ctypes.c_void_p()



    def Init_Camera(self):
        EDSDK.EdsInitializeSDK()
        EdsCameraListRef = ctypes.c_void_p(None)
        EDSDK.EdsGetCameraList(ctypes.byref(EdsCameraListRef))
        EDSDK.EdsGetChildAtIndex(EdsCameraListRef, 0, ctypes.byref(self.CameraRef))
        EDSDK.EdsOpenSession(self.CameraRef)

    def set_LiveView_ready(self):
        kEdsPropID_Evf_OutputDevice = 0x00000500
        outPropertyData = ctypes.c_int(2)
        EDSDK.EdsSetPropertyData(self.CameraRef, kEdsPropID_Evf_OutputDevice, 0, ctypes.sizeof(outPropertyData), ctypes.byref(outPropertyData))

    # get single Live image, should be in a loop
    def get_Live_image(self):
        LiveStream = ctypes.c_void_p()
        evfImage = ctypes.c_void_p()
        EDSDK.EdsCreateMemoryStream(ctypes.c_ulonglong(0), ctypes.byref(LiveStream))
        EDSDK.EdsCreateEvfImageRef(LiveStream, ctypes.byref(evfImage))
        Pointer = ctypes.pointer(ctypes.c_ubyte())
        imageLen = ctypes.c_ulonglong()
        EDSDK.EdsDownloadEvfImage(self.CameraRef, evfImage)
        EDSDK.EdsGetPointer(LiveStream, ctypes.byref(Pointer))
        EDSDK.EdsGetLength(LiveStream, ctypes.byref(imageLen))
        imageData = numpy.ctypeslib.as_array(ctypes.cast(Pointer, ctypes.POINTER(ctypes.c_ubyte)), (imageLen.value,))
        EDSDK.EdsRelease(LiveStream)
        EDSDK.EdsRelease(evfImage)
        if (imageData.size != 0) and (imageData[0] != 0):
            return jpeg.decode(imageData)

    def set_Capture_ready(self):
        kEdsObjectEvent_All = 0x00000200
        EDSDK.EdsSetObjectEventHandler(self.CameraRef, kEdsObjectEvent_All, ObjectHandler, None)
        kEdsPropID_SaveTo = 0x0000000b
        kEdsSaveTo_Host = ctypes.c_int(2)
        EDSDK.EdsSetPropertyData(self.CameraRef, kEdsPropID_SaveTo, 0, ctypes.sizeof(kEdsSaveTo_Host), ctypes.byref(kEdsSaveTo_Host))
        cap = EdsCapacity(0x7FFFFFFF, 0x1000, 1)
        EDSDK.EdsSetCapacity(self.CameraRef, cap)

    def get_Capture_image(self):
        main_thread_id = win32api.GetCurrentThreadId()
        def on_timer():
            win32api.PostThreadMessage(main_thread_id, win32con.WM_QUIT, 0, 0)
        t = Timer(5, on_timer)  # Quit after 5 seconds
        t.start()
        EDSDK.EdsSendCommand(self.CameraRef, 0, 0)
        win32gui.PumpMessages()

    def Terminate(self):
        EDSDK.EdsCloseSession(self.CameraRef)
        EDSDK.EdsTerminateSDK()

