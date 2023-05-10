# test python script must be in same location as aurum_pb2.py

import grpc
from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import time
import argparse

isScrollableBase1PageOpened = False


# Check if notification test1 page is opened or not.
def CheckScrollableBase1TestStart(stub):
    LaunchAppTest(stub)

    global isScrollableBase1PageOpened
    isScrollableBase1PageOpened = FindTCByInputText(stub, "ScrollableBaseTest1")
    time.sleep(0.3)
    return isScrollableBase1PageOpened


# Check
def CheckScrollableBase11(stub):
    if not isScrollableBase1PageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button'))
    for elem in res.elements:
        if "Change Property" in elem.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/ScrollableBase/ScrollableBaseTest11.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/ScrollableBase/ScrollableBaseTest11.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check
def CheckScrollableBase12(stub):
    if not isScrollableBase1PageOpened:
        return False

    if TAP(stub, "ScrollableBase") is False:
        return False

    FLICK_RIGHT(stub)

    # Take screenshot
    screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/ScrollableBase/ScrollableBaseTest12.png")
    if screenShort is None:
        return False

    # Read image file expected
    expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/ScrollableBase/ScrollableBaseTest12.png')
    if expectedScreenShot is None:
        return False

    # Check ssim
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def FLICK_RIGHT(stub):
    # geometry
    # {
    #     x: 480
    #     y: 205
    #     width: 960
    #     height: 360
    # }
    stub.flick(ReqFlick(startPoint=Point(x=1000, y=300), endPoint=Point(x=480, y=300), durationMs=110))
    time.sleep(0.3)


def TAP(stub, type):
    return TAP_BY_NAME(stub, type)


def TAP_BY_NAME(stub, type):
    id = findWidget(stub, type)
    if id:
        return True
    else:
        return False


def findWidget(stub, type):
    res = stub.findElements(ReqFindElements(widgetType=type))
    for elem in res.elements:
        if "scrollableBase" in elem.text:
            targetId = elem.elementId
            return targetId


def CheckScrollableBase1TestEnd(stub):
    global isScrollableBase1PageOpened
    isScrollableBase1PageOpened = False

    # Return to NUI Gallery page.
    ClickBackButton(stub)
    time.sleep(0.3)

    # Exit Gallery.
    ExitApp(stub)
    time.sleep(0.3)
    return True


def runTest(stub, testFunc):
    print("Testing started :", testFunc.__name__)
    result = testFunc(stub)
    print("Testing {} result : {}".format(testFunc.__name__, result))

    return True


def run():
    with grpc.insecure_channel('localhost:50051', options=(('grpc.enable_http_proxy', 0),)) as channel:
        stub = BootstrapStub(channel)
        runTest(stub, CheckScrollableBase1TestStart)
        runTest(stub, CheckScrollableBase11)
        runTest(stub, CheckScrollableBase12)
        runTest(stub, CheckScrollableBase1TestEnd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Options')
    parser.add_argument('--exit', dest='exit', action='store_true')
    parser.add_argument('--no-exit', dest='exit', action='store_false')
    parser.set_defaults(exit=True)
    args = parser.parse_args()
    run()
