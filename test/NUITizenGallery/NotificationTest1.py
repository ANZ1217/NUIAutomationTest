# test python script must be in same location as aurum_pb2.py

import grpc
from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import time

isNotificationPageOpened = False


# Check if notification test1 page is opened or not.
def CheckNotificationTestStart(stub):
    if not LaunchAppTest(stub):
        return False

    global isNotificationPageOpened
    isNotificationPageOpened = FindTCByInputText(stub, "NotificationTest1")
    time.sleep(0.3)
    return isNotificationPageOpened


# Check Dismiss
def CheckNotificationTest1(stub):
    if not isNotificationPageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button'))
    for elem in res.elements:
        if "Dismiss" in elem.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="Notification/NotificationTest1.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='Notification/NotificationTestExpected1.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check ForceQuit
def CheckNotificationTest2(stub):
    if not isNotificationPageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button'))
    for elem in res.elements:
        if "ForceQuit" in elem.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="Notification/NotificationTest2.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='Notification/NotificationTestExpected2.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckNotificationTestEnd(stub):
    global isNotificationPageOpened
    isNotificationPageOpened = False

    # Return to NUI Gallery page.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Exit Gallery.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='XF86Exit'))
    time.sleep(0.3)

    if stub.getAppInfo(ReqGetAppInfo(packageName='org.tizen.example.NUITizenGallery')).isRunning:
        stub.closeApp(ReqCloseApp(packageName='org.tizen.example.NUITizenGallery'))
    return True


def ReLaunch(stub):
    # Return to NUI Gallery page.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    FindTCByInputText(stub, "NotificationTest1")
    return True


def runTest(stub, testFunc):
    print("Testing started :", testFunc)
    result = testFunc(stub)
    print("Testing result :", result)
    return True


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = BootstrapStub(channel)
        runTest(stub, CheckNotificationTestStart)
        runTest(stub, CheckNotificationTest1)
        runTest(stub, ReLaunch)
        runTest(stub, CheckNotificationTest2)
        runTest(stub, CheckNotificationTestEnd)


if __name__ == '__main__':
    run()
