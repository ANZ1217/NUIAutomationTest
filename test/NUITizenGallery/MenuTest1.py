# test python script must be in same location as aurum_pb2.py

from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import grpc
import time
import argparse

isMenuPageOpened = False

# Check if Menu page is opened or not.
def CheckMenuTestStart(stub):
    if not LaunchAppTest(stub):
        return False

    global isMenuPageOpened
    isMenuPageOpened = FindTCByInputText(stub, "MenuTest1")
    time.sleep(0.3)
    return isMenuPageOpened


# Check if Menu is shown or not.
def CheckMenuTest11(stub):
    if not isMenuPageOpened:
        return False

    # Move focus to the button "Show Menu".
    if(FindButtonandClickByText(stub, 'Show Menu') == False):
        return False

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/Menu/MenuTest11.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/Menu/MenuTest11.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check if Menu is dismissed or not.
def CheckMenuTest12(stub):
    if not isMenuPageOpened:
        return False

    # Move focus to the button "Dismiss Menu".
    if(FindButtonandClickByText(stub, 'Dismiss Menu') == False):
        return False

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/Menu/MenuTest12.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/Menu/MenuTest12.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check if Menu exit normally.
def CheckMenuTestEnd(stub):

    # Press to NUI Gallery page.
    ClickBackButton(stub)
    time.sleep(0.3)

    # Exit Gallery.
    ExitApp(stub)
    time.sleep(2)
    return True


def runTest(stub, testFunc):
    print("Testing started :", testFunc.__name__)
    result = testFunc(stub)
    print("Testing {} result : {}".format(testFunc.__name__, result))

    return True


def run():
    with grpc.insecure_channel('localhost:50051', options=(('grpc.enable_http_proxy', 0),)) as channel:
        stub = BootstrapStub(channel)
        runTest(stub, CheckMenuTestStart)
        runTest(stub, CheckMenuTest11)
        runTest(stub, CheckMenuTest12)
        runTest(stub, CheckMenuTestEnd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Options')
    parser.add_argument('--exit', dest='exit', action='store_true')
    parser.add_argument('--no-exit', dest='exit', action='store_false')
    parser.set_defaults(exit=True)
    args = parser.parse_args()
    run()
