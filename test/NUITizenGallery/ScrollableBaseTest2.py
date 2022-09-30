# test python script must be in same location as aurum_pb2.py

import grpc
from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import time
import argparse

isScrollableBase2PageOpened = False


# Check if notification test1 page is opened or not.
def CheckScrollableBase2TestStart(stub):
    LaunchAppTest(stub)

    global isScrollableBase2PageOpened
    isScrollableBase2PageOpened = FindTCByInputText(stub, "ScrollableBaseTest2")
    time.sleep(0.3)
    return isScrollableBase2PageOpened


# Check
def CheckScrollableBase21(stub):
    if not isScrollableBase2PageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button'))
    for elem in res.elements:
        if "ScrollTo" in elem.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))
            time.sleep(0.3)

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/ScrollableBase/ScrollableBaseTest21.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/ScrollableBase/ScrollableBaseTest21.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckScrollableBase22(stub):
    if not isScrollableBase2PageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button'))
    for elem in res.elements:
        if "ScrollToIndex" in elem.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/ScrollableBase/ScrollableBaseTest22.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/ScrollableBase/ScrollableBaseTest22.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckScrollableBase23(stub):
    if not isScrollableBase2PageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button'))
    for elem in res.elements:
        if "Remove" in elem.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/ScrollableBase/ScrollableBaseTest23.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/ScrollableBase/ScrollableBaseTest23.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckScrollableBase24(stub):
    if not isScrollableBase2PageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button'))
    for elem in res.elements:
        if "ReplaceLayout" in elem.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/ScrollableBase/ScrollableBaseTest24.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/ScrollableBase/ScrollableBaseTest24.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckScrollableBase25(stub):
    if not isScrollableBase2PageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button'))
    for elem in res.elements:
        if "SetScrollAvailableArea" in elem.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/ScrollableBase/ScrollableBaseTest25.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/ScrollableBase/ScrollableBaseTest25.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckScrollableBase26(stub):
    if not isScrollableBase2PageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button'))
    for elem in res.elements:
        if "RemoveAll" in elem.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/ScrollableBase/ScrollableBaseTest26.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/ScrollableBase/ScrollableBaseTest26.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckScrollableBase2TestEnd(stub):
    global isScrollableBase2PageOpened
    isScrollableBase2PageOpened = False

    # Return to NUI Gallery page.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Exit Gallery.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='XF86Exit'))
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
        runTest(stub, CheckScrollableBase2TestStart)
        runTest(stub, CheckScrollableBase21)
        runTest(stub, CheckScrollableBase22)
        runTest(stub, CheckScrollableBase23)
        runTest(stub, CheckScrollableBase24)
        runTest(stub, CheckScrollableBase25)
        runTest(stub, CheckScrollableBase26)
        runTest(stub, CheckScrollableBase2TestEnd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Options')
    parser.add_argument('--exit', dest='exit', action='store_true')
    parser.add_argument('--no-exit', dest='exit', action='store_false')
    parser.set_defaults(exit=True)
    args = parser.parse_args()
    run()
