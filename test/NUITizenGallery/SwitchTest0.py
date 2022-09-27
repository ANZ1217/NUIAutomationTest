# test python script must be in same location as aurum_pb2.py

import grpc
from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import time
import argparse

isSwitchPageOpened = False


# Check if switch test page is opened or not.
def CheckSwitchTestStart(stub):
    if not LaunchAppTest(stub):
        return False

    global isSwitchPageOpened
    isSwitchPageOpened = FindTCByInputText(stub, "SwitchTest")
    time.sleep(1)
    return isSwitchPageOpened


# Check BackgroundImageURLSelector
def CheckSwitchTest1(stub):
    if not isSwitchPageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button'))
    for elem in res.elements:
        if "SwitchBackgroundImageURLSelector" in elem.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))
            time.sleep(1)

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/Switch/SwitchTest01.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/Switch/SwitchTest01.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check SwitchHandlerImageURL and SwitchHandlerImageSize
def CheckSwitchTest2(stub):
    if not isSwitchPageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button'))
    for elem in res.elements:
        if "SwitchHandlerImageURL & Size" in elem.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))
            time.sleep(1)

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/Switch/SwitchTest02.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/Switch/SwitchTest02.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check SwitchHandlerImageURLSelector
def CheckSwitchTest3(stub):
    if not isSwitchPageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button', isShowing=True))
    for elem in res.elements:
        if "SwitchHandlerImageURLSelector" in elem.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))
            time.sleep(1)

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/Switch/SwitchTest03.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/Switch/SwitchTest03.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check SelectedChanged
def CheckSwitchTest4(stub):
    if not isSwitchPageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='SwitchImpl', isShowing=True))
    # print("res=", res)
    for elem in res.elements:
        stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))
        time.sleep(1)

        # Take screenshot
        screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/Switch/SwitchTest04.png")
        if screenShort is None:
            return False

        # Read image file expected
        expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/Switch/SwitchTest04.png')
        if expectedScreenShot is None:
            return False

        # Check ssim
        return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckSwitchTestEnd(stub):
    global isSwitchPageOpened
    isSwitchPageOpened = False

    # Return to NUI Gallery page.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(1)

    # Exit Gallery.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='XF86Exit'))
    time.sleep(2)
    return True


def runTest(stub, testFunc):
    print("Testing started :", testFunc)
    result = testFunc(stub)
    print("Testing result :", result)
    return True


def run():
    with grpc.insecure_channel('localhost:50051', options=(('grpc.enable_http_proxy', 0),)) as channel:
        stub = BootstrapStub(channel)
        time.sleep(1)
        runTest(stub, CheckSwitchTestStart)
        runTest(stub, CheckSwitchTest1)
        runTest(stub, CheckSwitchTest2)
        runTest(stub, CheckSwitchTest3)
        runTest(stub, CheckSwitchTest4)
        runTest(stub, CheckSwitchTestEnd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Options')
    parser.add_argument('--exit', dest='exit', action='store_true')
    parser.add_argument('--no-exit', dest='exit', action='store_false')
    parser.set_defaults(exit=True)
    args = parser.parse_args()
    run()
