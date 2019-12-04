import ctypes
import os
import numpy
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
        err = EDSDK.EdsGetDirectoryItemInfo(Ref, ctypes.byref(dirinfo))
        if err:
            print("get directoryItemInfo failed with error code ", err)
            return

        stream = ctypes.c_void_p()
        err = EDSDK.EdsCreateFileStream(ImageFilename, kEdsFileCreateDisposition_CreateAlways, kEdsAccess_Write, ctypes.byref(stream))
        if err:
            print("create file stream failed with error code ", err)
            return

        err = EDSDK.EdsDownload(Ref, dirinfo.size, stream)
        if err:
            print("download file failed with error code ", err)
            return
        EDSDK.EdsDownloadComplete(Ref)
        EDSDK.EdsRelease(stream)
ObjectHandler = ObjectHandlerType(ObjectHandler_py)


class CanonCamera:

    def __init__(self):
        self.CameraRef = ctypes.c_void_p()



    def Init_Camera(self):
        err = EDSDK.EdsInitializeSDK()
        if err:
            print("initialize SDK failed with error code ", err)
            return
        EdsCameraListRef = ctypes.c_void_p(None)

        err = EDSDK.EdsGetCameraList(ctypes.byref(EdsCameraListRef))
        if err:
            print("get camera list failed with error code ", err)
            return

        err = EDSDK.EdsGetChildAtIndex(EdsCameraListRef, 0, ctypes.byref(self.CameraRef))
        if err:
            print("get cameraRaf failed with error code ", err)
            return



    def set_LiveView_ready(self):
        err = EDSDK.EdsOpenSession(self.CameraRef)
        if err:
            print("open session failed with error code ", err)
            return

        kEdsPropID_Evf_OutputDevice = 0x00000500
        outPropertyData = ctypes.c_int(2)
        err = EDSDK.EdsSetPropertyData(self.CameraRef, kEdsPropID_Evf_OutputDevice, 0, ctypes.sizeof(outPropertyData), ctypes.byref(outPropertyData))
        if err:
            print("set output device failed with error code ", err)
            return
        self.LiveStream = ctypes.c_void_p()
        self.evfImage = ctypes.c_void_p()
        err = EDSDK.EdsCreateMemoryStream(ctypes.c_ulonglong(0), ctypes.byref(self.LiveStream))
        if err:
            print("create memory stream failed with error code ", err)
            return

        err = EDSDK.EdsCreateEvfImageRef(self.LiveStream, ctypes.byref(self.evfImage))
        if err:
            print("create EvfImageRef failed with error code ", err)
            return

    # get single Live image, should be in a loop
    def get_Live_image(self):

        Pointer = ctypes.pointer(ctypes.c_ubyte())
        imageLen = ctypes.c_ulonglong()

        err = EDSDK.EdsDownloadEvfImage(self.CameraRef, self.evfImage)
        if err:
            print("download EvfImage failed with error code ", err)
            return

        EDSDK.EdsGetPointer(self.LiveStream, ctypes.byref(Pointer))
        EDSDK.EdsGetLength(self.LiveStream, ctypes.byref(imageLen))
        imageData = numpy.ctypeslib.as_array(ctypes.cast(Pointer, ctypes.POINTER(ctypes.c_ubyte)), (imageLen.value,))

        # if (imageData.size != 0) and (imageData[0] != 0):
        #     return jpeg.decode(imageData)
        return imageData

    def set_Capture_ready(self):
        err = EDSDK.EdsOpenSession(self.CameraRef)
        if err:
            print("open session failed with error code ", err)
            return

        kEdsObjectEvent_All = 0x00000200
        err = EDSDK.EdsSetObjectEventHandler(self.CameraRef, kEdsObjectEvent_All, ObjectHandler, None)
        if err:
            print("Set Object event handler failed with error code ", err)
            return

        kEdsPropID_SaveTo = 0x0000000b
        kEdsSaveTo_Host = ctypes.c_int(2)
        err = EDSDK.EdsSetPropertyData(self.CameraRef, kEdsPropID_SaveTo, 0, ctypes.sizeof(kEdsSaveTo_Host), ctypes.byref(kEdsSaveTo_Host))
        if err:
            print("Set SaveToHost failed with error code ", err)
            return

        cap = EdsCapacity(0x7FFFFFFF, 0x1000, 1)
        err = EDSDK.EdsSetCapacity(self.CameraRef, cap)
        if err:
            print("Set capacity failed with error code ", err)
            return

    def get_Capture_image(self):

        main_thread_id = win32api.GetCurrentThreadId()

        def on_timer():
            win32api.PostThreadMessage(main_thread_id, win32con.WM_QUIT, 0, 0)

        t = Timer(5, on_timer)  # Quit after 5 seconds
        t.start()
        err = EDSDK.EdsSendCommand(self.CameraRef, 0, 0)
        if err:
            print("Send command failed with error code ", err)
            return

        win32gui.PumpMessages()

    def Release_Live(self):
        EDSDK.EdsRelease(self.LiveStream)
        EDSDK.EdsRelease(self.evfImage)
        EDSDK.EdsCloseSession(self.CameraRef)

    def Terminate(self):

        EDSDK.EdsTerminateSDK()


