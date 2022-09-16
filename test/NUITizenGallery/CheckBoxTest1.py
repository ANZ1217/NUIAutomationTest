# test python script must be in same location as aurum_pb2.py

from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import grpc
import time

isCheckBoxPageOpened = False

# Check if CheckBox page is opened or not.
def CheckCheckBoxTestStart(stub):
    if not LaunchAppTest(stub):
        return False

    global isCheckBoxPageOpened
    isCheckBoxPageOpened = FindTCByInputText(stub, "CheckBoxTest1")
    time.sleep(0.3)
    return isCheckBoxPageOpened


# Check the first CheckBox.
def CheckCheckBoxTest11(stub):
    if not isCheckBoxPageOpened:
        return False

    # Move focus to the first checkbox.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Down'))
    time.sleep(0.3)

    # Press checkbox.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="CheckBox/CheckBoxTest11.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='CheckBox/CheckBoxTestExpected11.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check the second CheckBox.
def CheckCheckBoxTest12(stub):
    if not isCheckBoxPageOpened:
        return False

    # Move focus to the second CheckBox.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Down'))
    time.sleep(0.3)

    # Press checkbox.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="CheckBox/CheckBoxTest12.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='CheckBox/CheckBoxTestExpected12.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check if CheckBox exit normally.
def CheckCheckBoxTestEnd(stub):
    # Move focus to the back button of DialogPage launcher page.
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
        runTest(stub, CheckCheckBoxTestStart)
        runTest(stub, CheckCheckBoxTest11)
        runTest(stub, CheckCheckBoxTest12)
        runTest(stub, CheckCheckBoxTestEnd)


if __name__ == '__main__':                                         
    run()
