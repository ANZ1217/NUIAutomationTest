# test python script must be in same location as aurum_pb2.py

from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import grpc
import time
import argparse

isLoadingPageOpened = False

# Check if Loading page is opened or not.
def CheckLoadingTestStart(stub):
    if not LaunchAppTest(stub):
        return False

    global isLoadingPageOpened
    isLoadingPageOpened = FindTCByInputText(stub, "LoadingTest1")
    time.sleep(0.3)
    return isLoadingPageOpened


# Check the first loading.
def CheckLoadingTest11(stub):
    if not isLoadingPageOpened:
        return False

    # Move focus to the button "FPS++".
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Down'))
    time.sleep(0.3)

    # Press button.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Loading/LoadingTest11.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Loading/LoadingTestExpected11.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check the first loading.
def CheckLoadingTest12(stub):
    if not isLoadingPageOpened:
        return False

    # Move focus to the button "FPS++".
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Right'))
    time.sleep(0.3)

    # Press button.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Loading/LoadingTest12.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Loading/LoadingTestExpected12.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check the second loading.
def CheckLoadingTest13(stub):
    if not isLoadingPageOpened:
        return False

    # Move focus to the button "Pause".
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Down'))
    time.sleep(0.3)

    # Press button.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Loading/LoadingTest13.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Loading/LoadingTestExpected13.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check if Loading exit normally.
def CheckLoadingTestEnd(stub):
    # Move focus to the back button of Loading page.
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
        runTest(stub, CheckLoadingTestStart)
        runTest(stub, CheckLoadingTest11)
        runTest(stub, CheckLoadingTest12)
        runTest(stub, CheckLoadingTest13)
        runTest(stub, CheckLoadingTestEnd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Options')
    parser.add_argument('--exit', dest='exit', action='store_true')
    parser.add_argument('--no-exit', dest='exit', action='store_false')
    parser.set_defaults(exit=True)
    args = parser.parse_args()
    run()
