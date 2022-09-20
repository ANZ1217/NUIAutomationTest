# test python script must be in same location as aurum_pb2.py

from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import grpc
import time
import argparse

isButtonPageOpened = False

# Check if button test page is opened or not.
def CheckButtonTestStart(stub):
    if not LaunchAppTest(stub):
        return False

    global isButtonPageOpened
    isButtonPageOpened = FindTCByInputText(stub, "ButtonTest8")
    time.sleep(0.3)
    return isButtonPageOpened


# Check the first button.
def CheckButtonTest81(stub):
    if isButtonPageOpened == False:
        return False

    # Move focus to the first button.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Down'))
    time.sleep(0.3)

    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Down'))
    time.sleep(0.3)

    # Press button.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Button/ButtonTest81.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Button/ButtonTestExpected81.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check the second button.
def CheckButtonTest82(stub):
    if isButtonPageOpened == False:
        return False

    # Move focus to the second button.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Right'))
    time.sleep(0.3)

    # Press button.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Button/ButtonTest82.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Button/ButtonTestExpected82.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check the third button.
def CheckButtonTest83(stub):
    if isButtonPageOpened == False:
        return False

    # Move focus to the third button.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Down'))
    time.sleep(0.3)

    # Press button.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Button/ButtonTest83.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Button/ButtonTestExpected83.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check the fourth button.
def CheckButtonTest84(stub):
    if isButtonPageOpened == False:
        return False

    # Move focus to the fourth button.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Right'))
    time.sleep(0.3)

    # Press button.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Button/ButtonTest84.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Button/ButtonTestExpected84.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check if Button page exit normally.
def CheckButtonTestEnd(stub):
    # Move focus to the button 'Page 2' of the first page.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Up'))
    time.sleep(0.3)

    # Press to NUI Gallery page.
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
    with grpc.insecure_channel('localhost:50051', options=(('grpc.enable_http_proxy', 0),)) as channel:
        stub = BootstrapStub(channel)

        runTest(stub, CheckButtonTestStart)
        runTest(stub, CheckButtonTest81)
        runTest(stub, CheckButtonTest82)
        runTest(stub, CheckButtonTest83)
        runTest(stub, CheckButtonTest84)
        runTest(stub, CheckButtonTestEnd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Options')
    parser.add_argument('--exit', dest='exit', action='store_true')
    parser.add_argument('--no-exit', dest='exit', action='store_false')
    parser.set_defaults(exit=True)
    args = parser.parse_args()
    run()
