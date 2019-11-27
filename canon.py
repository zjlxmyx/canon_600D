import ctypes
import os
from ctypes import wintypes
import numpy
import cv2
from turbojpeg import TurboJPEG
import io
import time

os.environ['path'] += ';C:\\Users\\yanxin\\PycharmProjects\\canon_600D'
EDSDK = ctypes.cdll.LoadLibrary('C:\\Users\\yanxin\PycharmProjects\\canon_600D\\EDSDK.dll')

a = EDSDK.EdsInitializeSDK()

EdsCameraListRef = ctypes.c_void_p(None)
b = EDSDK.EdsGetCameraList(ctypes.byref(EdsCameraListRef))

count = ctypes.c_int()
c = EDSDK.EdsGetChildCount(EdsCameraListRef, ctypes.byref(count))

camera = ctypes.c_void_p()
d = EDSDK.EdsGetChildAtIndex(EdsCameraListRef, 0, ctypes.byref(camera))

e = EDSDK.EdsOpenSession(camera)

# VolumeRef = ctypes.c_void_p()
# f = EDSDK.EdsGetChildAtIndex(camera, 0, ctypes.byref(VolumeRef))
# EDSDK.EdsGetChildCount(VolumeRef, ctypes.byref(count))
#
#
# class VolumeInfo(ctypes.Structure):
#     _fields_ = [("storageType", ctypes.c_ulong),
#                 ("EdsAccess", ctypes.c_void_p),
#                 ("maxCapacity", ctypes.c_ulonglong),
#                 ("freeSpaceInBytes", ctypes.c_ulonglong),
#                 ("szVolumeLabel", ctypes.c_char),
#                 ]
#
#
# # Vinfo = VolumeInfo()
# # h = EDSDK.EdsGetVolumeInfo(VolumeRef, ctypes.byref(Vinfo))
#
# Directoryitem = ctypes.c_void_p()
# i = EDSDK.EdsGetChildAtIndex(VolumeRef, 0, ctypes.byref(Directoryitem))
# EDSDK.EdsGetChildCount(Directoryitem, ctypes.byref(count))
#
# folder = ctypes.c_void_p()
# j = EDSDK.EdsGetChildAtIndex(Directoryitem, 1, ctypes.byref(folder))
# EDSDK.EdsGetChildCount(folder, ctypes.byref(count))

# jj = EDSDK.EdsDeleteDirectoryItem(folder)

# file = folder = ctypes.c_void_p()
# k = EDSDK.EdsGetChildAtIndex(folder, 0, ctypes.byref(file))
#
# class DirectoryItemInfo(ctypes.Structure):
#     _fields_ = [("size", ctypes.c_ulonglong),
#                 ("isFolder", ctypes.c_bool),
#                 ("groupID", ctypes.c_ulong),
#                 ("option", ctypes.c_ulong),
#                 ("szFileName", ctypes.c_char),
#                 ("format", ctypes.c_ulong),
#                 ("dateTime", ctypes.c_ulong),
#                 ]
#
#
# DInfo = DirectoryItemInfo()
# ll = EDSDK.EdsGetDirectoryItemInfo(folder, ctypes.byref(DInfo))
#

# setzoom = ctypes.c_ulong(10)
# zoom = ctypes.c_ulong()
# kEdsPropID_Evf_Zoom = 0x00000507
#
# z = EDSDK.EdsSetPropertyData(camera, kEdsPropID_Evf_Zoom, 0, ctypes.sizeof(setzoom), ctypes.byref(setzoom))

#
outEdsDataType = ctypes.c_void_p()
outSize = ctypes.c_void_p()
kEdsPropID_Evf_OutputDevice = 0x00000500
m = EDSDK.EdsGetPropertySize(camera, kEdsPropID_Evf_OutputDevice, 0, ctypes.byref(outEdsDataType), ctypes.byref(outSize))

outPropertyData = ctypes.c_int(2)
n = EDSDK.EdsSetPropertyData(camera, kEdsPropID_Evf_OutputDevice, 0, outSize, ctypes.byref(outPropertyData))

stream = ctypes.c_void_p()
evfImage = ctypes.c_void_p()

o = EDSDK.EdsCreateMemoryStream(ctypes.c_ulonglong(0), ctypes.byref(stream))
# o = EDSDK.EdsCreateMemoryStream(ctypes.c_ulonglong(53747712), ctypes.byref(stream))
p = EDSDK.EdsCreateEvfImageRef(stream, ctypes.byref(evfImage))

Data = ctypes.c_ubyte()
imageData = ctypes.pointer(ctypes.c_ubyte())
imageLen = ctypes.c_ulonglong()
##def handleObjectEvent():
# EDSDK.EDSCALLBACK
##EDSDK.EdsSetObjectEventHandler(camera, 0x00000200, handleObjectEvent, ctypes.c_void_p())
# class EdsSize(ctypes.Structure):
#     _fields_ = [("width", ctypes.c_ulong),
#                 ("height", ctypes.c_ulong),
#                 ]
#
#
# imgsize = EdsSize()
# kEdsPropID_Evf_CoordinateSystem = 0x00000540

position = ctypes.c_ulonglong()

while True:
    q = EDSDK.EdsDownloadEvfImage(camera, evfImage)
    r = EDSDK.EdsGetPointer(stream, ctypes.byref(imageData))
    s = EDSDK.EdsGetLength(stream, ctypes.byref(imageLen))

    # t = EDSDK.EdsGetPropertyData(evfImage, kEdsPropID_Evf_CoordinateSystem, 0, ctypes.sizeof(imgsize), ctypes.byref(imgsize))
    # u = EDSDK.EdsGetPropertyData(evfImage, kEdsPropID_Evf_Zoom, 0, ctypes.sizeof(zoom), ctypes.byref(zoom))
    # print(Data)
    # v = EDSDK.EdsGetPosition(stream, ctypes.byref(position))
    # print(position)
    # zz = EDSDK.EdsGetPropertyData(evfImage, kEdsPropID_Evf_Zoom, 0, ctypes.sizeof(zoom), ctypes.byref(zoom))

    data = numpy.ctypeslib.as_array(ctypes.cast(imageData, ctypes.POINTER(ctypes.c_ubyte)),  (imageLen.value,))
    # data = numpy.ctypeslib.as_array(imageData, (518400,))
    # data.dtype = 'uint8'
    jpeg = TurboJPEG("C:\\turbojpeg.dll")
    if (data.size != 0) and (data[0] != 0):
        frame = jpeg.decode(data)
    #frame = numpy.reshape(data, (3456, 5184, 3))
    # # frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        cv2.imshow("SimpleLive_Python_uEye_OpenCV", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# f = EDSDK.EdsSendCommand(camera, 0x00000000, 0)

t = EDSDK.EdsCloseSession(camera)




EDSDK.EdsTerminateSDK()