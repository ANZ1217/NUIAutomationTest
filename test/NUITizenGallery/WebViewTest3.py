# test python script must be in same location as aurum_pb2.py
# Link of tested app is https://github.com/Samsung/TizenFX/tree/master/test/Tizen.NUI.WebViewTest

from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import grpc
import time
import argparse

isWebViewOpened = False

# Check if WebView page is opened or not.
def CheckWebViewTestStart(stub):
    if not LaunchAppTest(stub):
        return False

    global isWebViewOpened
    isWebViewOpened = FindTCByInputText(stub, "WebViewTest3")
    time.sleep(2)
    return isWebViewOpened


# Check green key.
def CheckWebViewTest11(stub):
    if not isWebViewOpened:
        return False

    # Move focus to WebView.
    for i in range(2):
        stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Down'))
        time.sleep(0.3)

    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='XF86Green'))
    time.sleep(2)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="WebView/WebViewTest31.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='WebView/WebViewTestExpected31.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check yellow key.
def CheckWebViewTest12(stub):
    if not isWebViewOpened:
        return False

    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='XF86Yellow'))
    time.sleep(2)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="WebView/WebViewTest32.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='WebView/WebViewTestExpected32.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check blue key.
def CheckWebViewTest13(stub):
    if not isWebViewOpened:
        return False

    for i in range(3):
        stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='XF86Blue'))
        time.sleep(2)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="WebView/WebViewTest33.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='WebView/WebViewTestExpected33.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check if WebView exit normally.
def CheckWebViewTestEnd(stub):
    # Exit Gallery.
    for i in range(2):
        stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='XF86Exit'))
        time.sleep(1)
    return True


def runTest(stub, testFunc):
    print("Testing started :", testFunc)
    result = testFunc(stub)
    print("Testing result :", result)
    return True


def run():
    with grpc.insecure_channel('localhost:50051', options=(('grpc.enable_http_proxy', 0),)) as channel:
        stub = BootstrapStub(channel)
        runTest(stub, CheckWebViewTestStart)
        runTest(stub, CheckWebViewTest11)
        runTest(stub, CheckWebViewTest12)
        runTest(stub, CheckWebViewTest13)
        runTest(stub, CheckWebViewTestEnd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Options')
    parser.add_argument('--exit', dest='exit', action='store_true')
    parser.add_argument('--no-exit', dest='exit', action='store_false')
    parser.set_defaults(exit=True)
    args = parser.parse_args()
    run()
