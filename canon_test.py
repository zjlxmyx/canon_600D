import ctypes
import os
from ctypes import wintypes
import numpy
import cv2
import time



os.environ['path'] += ';C:\\Users\\yanxin\\PycharmProjects\\canon_600D'
EDSDK = ctypes.cdll.LoadLibrary('C:\\Users\\yanxin\PycharmProjects\\canon_600D\\EDSDK.dll')
hr = False
a = EDSDK.EdsInitializeSDK()

EdsCameraListRef = ctypes.c_void_p(None)
b = EDSDK.EdsGetCameraList(ctypes.byref(EdsCameraListRef))

count = ctypes.c_int()
# c = EDSDK.EdsGetChildCount(EdsCameraListRef, ctypes.byref(count))

camera = ctypes.c_void_p()
d = EDSDK.EdsGetChildAtIndex(EdsCameraListRef, 0, ctypes.byref(camera))

e = EDSDK.EdsOpenSession(camera)

VolumeRef = ctypes.c_void_p()
f = EDSDK.EdsGetChildAtIndex(camera, 0, ctypes.byref(VolumeRef))
EDSDK.EdsGetChildCount(VolumeRef, ctypes.byref(count))


class VolumeInfo(ctypes.Structure):
    _fields_ = [("storageType", ctypes.c_ulong),
                ("EdsAccess", ctypes.c_void_p),
                ("maxCapacity", ctypes.c_ulonglong),
                ("freeSpaceInBytes", ctypes.c_ulonglong),
                ("szVolumeLabel", ctypes.c_char),
                ]


# Vinfo = VolumeInfo()
# h = EDSDK.EdsGetVolumeInfo(VolumeRef, ctypes.byref(Vinfo))

Directoryitem = ctypes.c_void_p()
i = EDSDK.EdsGetChildAtIndex(VolumeRef, 0, ctypes.byref(Directoryitem))
EDSDK.EdsGetChildCount(VolumeRef, ctypes.byref(count))

# folder = ctypes.c_void_p()
# j = EDSDK.EdsGetChildAtIndex(Directoryitem, 1, ctypes.byref(folder))
# EDSDK.EdsGetChildCount(folder, ctypes.byref(count))

# jj = EDSDK.EdsDeleteDirectoryItem(folder)

# file = folder = ctypes.c_void_p()
# k = EDSDK.EdsGetChildAtIndex(folder, 0, ctypes.byref(file))

class DirectoryItemInfo(ctypes.Structure):
    _fields_ = [("size", ctypes.c_ulonglong),
                ("isFolder", ctypes.c_bool),
                ("groupID", ctypes.c_ulong),
                ("option", ctypes.c_ulong),
                ("szFileName", ctypes.c_char),
                ("format", ctypes.c_ulong),
                ("dateTime", ctypes.c_ulong),
                ]


DInfo = DirectoryItemInfo()
ll = EDSDK.EdsGetDirectoryItemInfo(VolumeRef, ctypes.byref(DInfo))

print(VolumeRef)

t = EDSDK.EdsCloseSession(camera)




EDSDK.EdsTerminateSDK()