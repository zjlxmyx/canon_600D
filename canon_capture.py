import ctypes
import os
from ctypes import wintypes
import numpy
import cv2
from turbojpeg import TurboJPEG
import io
import time
import pythoncom
import win32gui

import win32api
import win32con
import pythoncom
from threading import Timer

main_thread_id = win32api.GetCurrentThreadId()


def on_timer():
    win32api.PostThreadMessage(main_thread_id, win32con.WM_QUIT, 0, 0)



os.environ['path'] += ';C:\\Users\\yanxin\\PycharmProjects\\canon_600D'
EDSDK = ctypes.cdll.LoadLibrary('C:\\Users\\yanxin\PycharmProjects\\canon_600D\\EDSDK.dll')
pythoncom.CoInitialize()

a = EDSDK.EdsInitializeSDK()

EdsCameraListRef = ctypes.c_void_p(None)
b = EDSDK.EdsGetCameraList(ctypes.byref(EdsCameraListRef))

count = ctypes.c_int()
c = EDSDK.EdsGetChildCount(EdsCameraListRef, ctypes.byref(count))

camera = ctypes.c_void_p()
d = EDSDK.EdsGetChildAtIndex(EdsCameraListRef, 0, ctypes.byref(camera))








class DirectoryItemInfo(ctypes.Structure):
    _fields_ = [("size", ctypes.c_ulonglong),
                ("isFolder", ctypes.c_bool),
                ("groupID", ctypes.c_ulong),
                ("option", ctypes.c_ulong),
                ("szFileName", ctypes.c_char*256),
                ("format", ctypes.c_ulong),
                ("dateTime", ctypes.c_ulong)]



kEdsObjectEvent_DirItemRequestTransfer = 0x00000208
global ImageFilename
# ImageFilename = ctypes.c_char*256
# ImageFilename.value = 'test.jpg'
ImageFilename = b'C:\\Users\\yanxin\\Desktop\\test.jpg'

ObjectHandlerType = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)
# EDSDK.EdsGetDirectoryItemInfo.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
# EDSDK.EdsDownload.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
# EDSDK.EdsDownloadComplete.argtypes = [ctypes.c_void_p]
# EDSDK.EdsCreateFileStream.a


def ObjectHandler_py(event,object,context):

    if event == kEdsObjectEvent_DirItemRequestTransfer:

        dirinfo = DirectoryItemInfo()
        object = ctypes.c_void_p(object)

        # pointer = ctypes.byref(dirinfo)
        f = EDSDK.EdsGetDirectoryItemInfo(object, ctypes.byref(dirinfo))
        stream = ctypes.c_void_p()
        kEdsFileCreateDisposition_CreateAlways = 1
        kEdsAccess_Write = 2
        g = EDSDK.EdsCreateFileStream(ImageFilename, kEdsFileCreateDisposition_CreateAlways, kEdsAccess_Write, ctypes.byref(stream))
        h = EDSDK.EdsDownload(object, dirinfo.size, stream)
        i = EDSDK.EdsDownloadComplete(object)
        j = EDSDK.EdsRelease(stream)
        print(object)
        print(stream)
        print(dirinfo)
        print(f, g, h, i, j)

    return 0
ObjectHandler = ObjectHandlerType(ObjectHandler_py)


kEdsObjectEvent_All = 0x00000200
k = EDSDK.EdsSetObjectEventHandler(camera, kEdsObjectEvent_All, ObjectHandler, None)

EDSDK.EdsOpenSession.argtypes = [ctypes.c_void_p]
e = EDSDK.EdsOpenSession(camera)

kEdsPropID_SaveTo = 0x0000000b
kEdsSaveTo_Host = ctypes.c_int(2)
data = ctypes.c_int()
n = EDSDK.EdsSetPropertyData(camera, kEdsPropID_SaveTo, 0, ctypes.sizeof(kEdsSaveTo_Host), ctypes.byref(kEdsSaveTo_Host))
o = EDSDK.EdsGetPropertyData(camera, kEdsPropID_SaveTo, 0, ctypes.sizeof(data), ctypes.byref(data))


class EdsCapacity(ctypes.Structure):
    _fields_ = [("numberOfFreeClusters", ctypes.c_ulong),
                ("bytesPerSector", ctypes.c_ulong),
                ("reset", ctypes.c_bool)]

cap = EdsCapacity(0x7FFFFFFF, 0x1000, 1)
p = EDSDK.EdsSetCapacity(camera, cap)

t = Timer(5, on_timer)  # Quit after 5 seconds
t.start()

print(a,b,c,d,e,k,n,o,p)
l = EDSDK.EdsSendCommand(camera, 0, 0)

win32gui.PumpMessages()


m = EDSDK.EdsCloseSession(camera)
EDSDK.EdsTerminateSDK()
