# test python script must be in same location as aurum_pb2.py

import grpc
from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import time
import argparse

isTabContentPageOpened = False


# Check if notification test1 page is opened or not.
def CheckTabContentTestStart(stub):
    LaunchAppTest(stub)

    global isTabContentPageOpened
    isTabContentPageOpened = FindTCByInputText(stub, "TabContentTest")
    time.sleep(0.3)
    return isTabContentPageOpened


# Check
def CheckTabContentTest1(stub):
    if not isTabContentPageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button', isShowing=True))
    for elem in res.elements:
        if "OnSelect" in elem.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))
            time.sleep(1)

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/TabContent/TabContentTest01.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/TabContent/TabContentTest01.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckTabContentTestEnd(stub):
    global isTabContentPageOpened
    isTabContentPageOpened = False

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
        runTest(stub, CheckTabContentTestStart)
        runTest(stub, CheckTabContentTest1)
        runTest(stub, CheckTabContentTestEnd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Options')
    parser.add_argument('--exit', dest='exit', action='store_true')
    parser.add_argument('--no-exit', dest='exit', action='store_false')
    parser.set_defaults(exit=True)
    args = parser.parse_args()
    run()
