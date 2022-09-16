# test python script must be in same location as aurum_pb2.py

from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import grpc
import time

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
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Down'))
    time.sleep(0.3)

    # Press button.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Menu/MenuTest11.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Menu/MenuTestExpected11.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check if Menu is dismissed or not.
def CheckMenuTest12(stub):
    if not isMenuPageOpened:
        return False

    # Move focus to the button "Dismiss Menu".
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Right'))
    time.sleep(0.3)

    # Press button.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Menu/MenuTest12.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Menu/MenuTestExpected12.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check if Menu exit normally.
def CheckMenuTestEnd(stub):
    # Move focus to the back button.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Up'))
    time.sleep(0.3)

    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Up'))
    time.sleep(0.3)

    # Press to NUI Gallery page.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

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
        runTest(stub, CheckMenuTestStart)
        runTest(stub, CheckMenuTest11)
        runTest(stub, CheckMenuTest12)
        runTest(stub, CheckMenuTestEnd)


if __name__ == '__main__':
    run()
