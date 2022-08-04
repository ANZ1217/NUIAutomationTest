# test python script must be in same location as aurum_pb2.py

import grpc
from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import time

isProgressbarPageOpened = False
SCREEN_WIDTH = 0
XPos = 0
YPos = 0


# Check if notification test1 page is opened or not.
def CheckProgressbarTestStart(stub):
    if not LaunchAppTest(stub):
        return False

    global isProgressbarPageOpened
    isProgressbarPageOpened = FindTCByInputText(stub, "ProgressbarTest2")
    time.sleep(0.3)
    return isProgressbarPageOpened


# Check TrackColor, BufferImageURL, BufferValue, BufferColor, ProgressState
def CheckProgressbarTest1(stub):
    if not isProgressbarPageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button', isShowing=True))
    for elem in res.elements:
        if "Animate" in elem.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))
            time.sleep(4)

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="Progressbar/ProgressbarTest1.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='Progressbar/ProgressbarTestExpected1.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check
def CheckProgressbarTest2(stub):
    if not isProgressbarPageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Slider', isShowing=True))
    for elem in res.elements:
        global SCREEN_WIDTH, YPos, XPos
        SCREEN_WIDTH = elem.geometry.width
        XPos = int(SCREEN_WIDTH * 3 / 10)
        YPos = elem.geometry.y
        print("SCREEN_WIDTH = ", SCREEN_WIDTH)
        print("XPos = ", XPos)
        print("YPos = ", YPos)

        FLICK_RIGHT(stub)
        time.sleep(1)

        # Take screenshot
        screenShort = ReadScreenShotFile(stub, fileName="Progressbar/ProgressbarTest2.png")
        if screenShort is None:
            return False

        # Read image file expected
        expectedScreenShot = ReadImageFile(fileName='Progressbar/ProgressbarTestExpected2.png')
        if expectedScreenShot is None:
            return False

        # Check ssim
        return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check CurrentValue
def CheckProgressbarTest3(stub):
    if not isProgressbarPageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button', isShowing=True))
    for elem in res.elements:
        if "+" in elem.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))
            time.sleep(1)
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))
            time.sleep(1)

        if "-" in elem.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="Progressbar/ProgressbarTest3.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='Progressbar/ProgressbarTestExpected3.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check IndeterminateImageUrl
def CheckProgressbarTest4(stub):
    if not isProgressbarPageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button', isShowing=True))
    for elem in res.elements:
        if "ChangeIndeterminateImageUrl" in elem.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))
            time.sleep(1)

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="Progressbar/ProgressbarTest4.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='Progressbar/ProgressbarTestExpected4.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def FLICK_RIGHT(stub):
    stub.flick(ReqFlick(startPoint=Point(x=YPos, y=YPos), endPoint=Point(x=YPos+290, y=YPos), durationMs=110))
    time.sleep(1)


def CheckProgressbarTestEnd(stub):
    global isProgressbarPageOpened
    isProgressbarPageOpened = False

    # Return to NUI Gallery page.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Exit Gallery.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='XF86Exit'))
    time.sleep(0.3)

    if stub.getAppInfo(ReqGetAppInfo(packageName='org.tizen.example.NUITizenGallery')).isRunning:
        stub.closeApp(ReqCloseApp(packageName='org.tizen.example.NUITizenGallery'))
    return True


def runTest(stub, testFunc):
    print("Testing started :", testFunc)
    result = testFunc(stub)
    print("Testing result :", result)
    return True


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = BootstrapStub(channel)
        runTest(stub, CheckProgressbarTestStart)
        runTest(stub, CheckProgressbarTest1)
        runTest(stub, CheckProgressbarTest2)
        runTest(stub, CheckProgressbarTest3)
        runTest(stub, CheckProgressbarTest4)
        runTest(stub, CheckProgressbarTestEnd)


if __name__ == '__main__':
    run()
