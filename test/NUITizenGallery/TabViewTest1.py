# test python script must be in same location as aurum_pb2.py

import grpc
from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import time

isTabViewPageOpened = False


# Check if notification test1 page is opened or not.
def CheckTabViewTestStart(stub):
    LaunchAppTest(stub)

    global isTabViewPageOpened
    isTabViewPageOpened = FindTCByInputText(stub, "TabViewTest1")
    time.sleep(0.3)
    return isTabViewPageOpened


# Check
def CheckTabViewTest1(stub):
    if not isTabViewPageOpened:
        return False

    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Down'))
    time.sleep(0.3)

    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Right'))
    time.sleep(0.3)

    # Press TabButton.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Take ScreenShot.
    screenShort = ReadScreenShotFile(stub, fileName="TabView/TabViewTest1.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='TabView/TabViewTestExpected1.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckTabViewTest2(stub):
    if not isTabViewPageOpened:
        return False

    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Right'))
    time.sleep(0.3)

    # Press TabButton.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Take ScreenShot.
    screenShort = ReadScreenShotFile(stub, fileName="TabView/TabViewTest2.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='TabView/TabViewTestExpected2.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckTabViewTest3(stub):
    if not isTabViewPageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button', isShowing=True))
    for elem in res.elements:
        if "Remove Tab3" in elem.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))
            time.sleep(1)

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="TabView/TabViewTest3.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='TabView/TabViewTestExpected3.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckTabViewTestEnd(stub):
    global isTabViewPageOpened
    isTabViewPageOpened = False

    # Return to NUI Gallery page.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Exit Gallery.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='XF86Exit'))
    time.sleep(0.3)
    return True


def runTest(stub, testFunc):
    print("Testing started :", testFunc)
    result = testFunc(stub)
    print("Testing result :", result)
    return True


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = BootstrapStub(channel)
        runTest(stub, CheckTabViewTestStart)
        runTest(stub, CheckTabViewTest1)
        runTest(stub, CheckTabViewTest2)
        runTest(stub, CheckTabViewTest3)
        runTest(stub, CheckTabViewTestEnd)


if __name__ == '__main__':
    run()
