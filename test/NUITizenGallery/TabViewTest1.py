# test python script must be in same location as aurum_pb2.py

import grpc
from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import time
import argparse

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

    # Press TabButton.
    if(FindButtonandClickByText(stub, 'Tab1') == False):
        return False

    # Take ScreenShot.
    screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/TabView/TabViewTest1.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/TabView/TabViewTest1.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckTabViewTest2(stub):
    if not isTabViewPageOpened:
        return False

    # Press TabButton.
    if(FindButtonandClickByText(stub, 'Tab2') == False):
        return False

    # Take ScreenShot.
    screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/TabView/TabViewTest2.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/TabView/TabViewTest2.png')
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
            screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/TabView/TabViewTest3.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/TabView/TabViewTest3.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckTabViewTestEnd(stub):
    global isTabViewPageOpened
    isTabViewPageOpened = False

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
        runTest(stub, CheckTabViewTestStart)
        runTest(stub, CheckTabViewTest1)
        runTest(stub, CheckTabViewTest2)
        runTest(stub, CheckTabViewTest3)
        runTest(stub, CheckTabViewTestEnd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Options')
    parser.add_argument('--exit', dest='exit', action='store_true')
    parser.add_argument('--no-exit', dest='exit', action='store_false')
    parser.set_defaults(exit=True)
    args = parser.parse_args()
    run()
