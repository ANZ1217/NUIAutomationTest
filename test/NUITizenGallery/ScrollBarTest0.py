# test python script must be in same location as aurum_pb2.py

import grpc
from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import time
import argparse

isScrollbarPageOpened = False


# Check if notification test1 page is opened or not.
def CheckScrollBarTestStart(stub):
    LaunchAppTest(stub)

    global isScrollbarPageOpened
    isScrollbarPageOpened = FindTCByInputText(stub, "ScrollBarTest")
    time.sleep(0.3)
    return isScrollbarPageOpened


# Check
def CheckScrollBarTest1(stub):
    if not isScrollbarPageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button', isShowing=True))
    for elem in res.elements:
        if "+" in elem.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))
            time.sleep(1)

            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))
            time.sleep(1)

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/ScrollBar/ScrollBarTest01.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/ScrollBar/ScrollBarTest01.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckScrollBarTest2(stub):
    if not isScrollbarPageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button', isShowing=True))
    for elem in res.elements:
        if "-" in elem.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))
            time.sleep(1)

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/ScrollBar/ScrollBarTest02.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/ScrollBar/ScrollBarTest02.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckScrollBarTest3(stub):
    if not isScrollbarPageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button', isShowing=True))
    for elem in res.elements:
        if "ScrollMove" in elem.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))
            time.sleep(1)

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/ScrollBar/ScrollBarTest03.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/ScrollBar/ScrollBarTest03.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckScrollBarTest4(stub):
    if not isScrollbarPageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button', isShowing=True))
    for elem in res.elements:
        if "ScrollUpdate" in elem.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))
            time.sleep(1)

            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))
            time.sleep(1)

            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))
            time.sleep(1)

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/ScrollBar/ScrollBarTest04.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/ScrollBar/ScrollBarTest04.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckScrollBarTestEnd(stub):
    global isScrollbarPageOpened
    isScrollbarPageOpened = False

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
        runTest(stub, CheckScrollBarTestStart)
        runTest(stub, CheckScrollBarTest1)
        runTest(stub, CheckScrollBarTest2)
        runTest(stub, CheckScrollBarTest3)
        runTest(stub, CheckScrollBarTest4)
        runTest(stub, CheckScrollBarTestEnd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Options')
    parser.add_argument('--exit', dest='exit', action='store_true')
    parser.add_argument('--no-exit', dest='exit', action='store_false')
    parser.set_defaults(exit=True)
    args = parser.parse_args()
    run()
