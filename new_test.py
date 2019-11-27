from ctypes import *
import pythoncom
import datetime
import os

os.environ['path'] += ';C:\\Users\\yanxin\\PycharmProjects\\canon_600D'
edsdk = cdll.LoadLibrary('C:\\Users\\yanxin\\PycharmProjects\\canon_600D\\EDSDK.dll')

global aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, mm, nn

def AddTime(fname):
    now = datetime.datetime.now()
    nname = fname[:-4] + '_' + now.isoformat()[:-7].replace(':', '-') + fname[-4:]
    return nname


class EDSDKError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def EDErrorMsg(code):
    return "EDSDK error code" + hex(code)




def Release(ref):
    edsdk.EdsRelease(ref)


def GetChildCount(ref):
    i = c_int()
    aa = edsdk.EdsGetChildCount(ref, byref(i))
    return i.value


def GetChild(ref, number):
    c = c_void_p()
    bb = edsdk.EdsGetChildAtIndex(ref, number, byref(c))
    return c


kEdsObjectEvent_DirItemRequestTransfer = 0x00000208
kEdsObjectEvent_DirItemCreated = 0x00000204

ObjectHandlerType = WINFUNCTYPE(c_int, c_int, c_void_p, c_void_p)
edsdk.EdsGetDirectoryItemInfo.argtypes = [c_int64, c_void_p]
edsdk.EdsDownload.argtypes = [c_int64, c_int, c_void_p]
edsdk.EdsDownloadComplete.argtypes = [c_int64]

def ObjectHandler_py(event, image, context):
    if event == kEdsObjectEvent_DirItemRequestTransfer:
        dirinfo = DirectoryItemInfo()
        cc = edsdk.EdsGetDirectoryItemInfo(image, byref(dirinfo))
        stream = c_void_p()

        dd = edsdk.EdsCreateFileStream(ImageFilename, 1, 2, byref(stream))

        ee = edsdk.EdsDownload(image, dirinfo.size, stream)
        ff = edsdk.EdsDownloadComplete(image)
        Release(stream)
        print(cc,dd,ee,ff)

        global WaitingForImage
        WaitingForImage = False
    return 0


ObjectHandler = ObjectHandlerType(ObjectHandler_py)

# kEdsStateEvent_WillSoonShutDown = 0x00000303
#
# StateHandlerType = WINFUNCTYPE(c_int, c_int, c_int, c_void_p)
#
#
# def StateHandler_py(event, state, context):
#     if event == kEdsStateEvent_WillSoonShutDown:
#         print("cam about to shut off")
#         Call(edsdk.EdsSendCommand(context, 1, 0))
#     return 0
#
#
# StateHandler = StateHandlerType(StateHandler_py)
#
# PropertyHandlerType = WINFUNCTYPE(c_int, c_int, c_int, c_int, c_void_p)


# def PropertyHandler_py(event, property, param, context):
#     return 0
#
#
# PropertyHandler = PropertyHandlerType(PropertyHandler_py)


class DirectoryItemInfo(Structure):
    _fields_ = [("size", c_ulonglong),
                ("isFolder", c_bool),
                ("groupID", c_ulong),
                ("option",c_ulong),
                ("szFileName", c_char*256),
                ("format", c_ulong),
                ("dateTime", c_ulong)]


WaitingForImage = False
ImageFilename = None


# def DownloadImage(image):
#     dirinfo = DirectoryItemInfo()
#     cc = edsdk.EdsGetDirectoryItemInfo(image, byref(dirinfo))
#     stream = c_void_p()
#
#
#     dd = edsdk.EdsCreateFileStream(ImageFilename, 1, 2, byref(stream))
#
#     ee = edsdk.EdsDownload(image, dirinfo.size, stream)
#     ff = edsdk.EdsDownloadComplete(image)
#     Release(stream)
#
#     global WaitingForImage
#     WaitingForImage = False


kEdsSaveTo_Camera = 1
kEdsSaveTo_Host = 2
kEdsSaveTo_Both = kEdsSaveTo_Camera | kEdsSaveTo_Host
kEdsPropID_SaveTo = 0x0000000b


class EdsCapacity(Structure):
    _fields_ = [("numberOfFreeClusters", c_int),
                ("bytesPerSector", c_int),
                ("reset", c_int)]


class Camera:
    def __init__(self, camnum=0):
        global ImageFilename
        # ImageFilename = c_char * 256
        # ImageFilename.value = 'C:\\Users\\yanxin\\Desktop\\test.jpg'
        ImageFilename = r'C:\Users\yanxin\Desktop\test.jpg'
        self.cam = None
        l = CameraList()
        self.cam = l.GetCam(camnum)
        gg = edsdk.EdsSetObjectEventHandler(self.cam, 0x200, ObjectHandler, None)
        # Call(edsdk.EdsSetPropertyEventHandler(self.cam, 0x100, PropertyHandler, None))
        # Call(edsdk.EdsSetCameraStateEventHandler(self.cam, 0x300, StateHandler, self.cam))
        hh = edsdk.EdsOpenSession(self.cam)

        self.SetProperty(kEdsPropID_SaveTo, kEdsSaveTo_Host)

        # set large capacity
        cap = EdsCapacity(10000000, 512, 1)
        ii = edsdk.EdsSetCapacity(self.cam, cap)

    def __del__(self):
        if self.cam is not None:
            jj = edsdk.EdsCloseSession(self.cam)
            kk = Release(self.cam)

    def SetProperty(self, property, param):
        d = c_int(param)
        ll = edsdk.EdsSetPropertyData(self.cam, property, 0, 4, byref(d))

    def AutoFocus(self):
        kEdsCameraCommand_ShutterButton_OFF = 0x00000000,
        #    kEdsCameraCommand_ShutterButton_Halfway                = 0x00000001,
        #    kEdsCameraCommand_ShutterButton_Completely            = 0x00000003,
        #    kEdsCameraCommand_ShutterButton_Halfway_NonAF        = 0x00010001,
        #    kEdsCameraCommand_ShutterButton_Completely_NonAF    = 0x00010003,
        # note that this can fail when AF fails (error code 0x8D01)
        self.SendCommand(4, 1)

    def Shoot(self, fname=None):
        # set saving flag
        global WaitingForImage
        WaitingForImage = True

        # note that this can fail when AF fails (error code 0x8D01)
        self.SendCommand(0)
        # capture succeeded so go on to download image
        while WaitingForImage:
            pythoncom.PumpWaitingMessages()
        return ImageFilename

    # def Shutter(self):
    #     self.SendCommand(4)
    #
    def KeepOn(self):
        # important command - keeps the camera connected when not used
        self.SendCommand(1)

    def SendCommand(self, command, param=0):
        # define kEdsCameraCommand_TakePicture                     0x00000000
        # define kEdsCameraCommand_ExtendShutDownTimer             0x00000001
        # define kEdsCameraCommand_BulbStart                          0x00000002
        # define kEdsCameraCommand_BulbEnd                          0x00000003
        # define kEdsCameraCommand_DoEvfAf                         0x00000102
        # define kEdsCameraCommand_DriveLensEvf                    0x00000103
        # define kEdsCameraCommand_DoClickWBEvf                    0x00000104
        # define kEdsCameraCommand_PressShutterButton              0x00000004
        nn = edsdk.EdsSendCommand(self.cam, command, param)


class CameraList:
    def __init__(self):
        self.list = c_void_p(None)
        mm = edsdk.EdsGetCameraList(byref(self.list))

    def Count(self):
        return GetChildCount(self.list)

    def GetCam(self, number=0):
        print
        "get cam"
        if self.Count() < (number + 1):
            print("Camera not found, make sure it's on and connected")
        return GetChild(self.list, number)

    def __del__(self):
        Release(self.list)


edsdk.EdsInitializeSDK()

if __name__ == "__main__":
    pythoncom.CoInitialize()
    c = Camera()
    from time import sleep

    c.Shoot()

    sleep(1)

    c.KeepOn()

    del c
    edsdk.EdsTerminateSDK()
    sleep(2)