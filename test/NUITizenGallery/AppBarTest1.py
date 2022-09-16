# test python script must be in same location as aurum_pb2.py

from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import grpc
import time

isAppBarPageOpened = False

# Check if AppBar test page is opened or not.
def CheckAppBarTestStart(stub):
    if not LaunchAppTest(stub):
        return False

    global isAppBarPageOpened
    isAppBarPageOpened = FindTCByInputText(stub, "AppBarTest1")
    return isAppBarPageOpened


# Check the first AppBar page.
def CheckAppBarTest11(stub):
    if isAppBarPageOpened == False:
        return False

    # Move focus to the button "Click to show AppBar".
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Down'))

    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Down'))

    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Down'))

    # Press button to the first page.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(1)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="AppBar/AppBarTest11.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='AppBar/AppBarTestExpected11.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check the second AppBar page.
def CheckAppBarTest12(stub):
    if isAppBarPageOpened == False:
        return False

    # Move focus to the button "Click to next".
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Down'))
    time.sleep(0.3)

    # Press button to the second page.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="AppBar/AppBarTest12.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='AppBar/AppBarTestExpected12.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check if AppBar exit normally.
def CheckAppBarTestEnd(stub):
    # Press button "Pop page" of the second page.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Move focus to the button 'Page 2' of the first page.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Up'))
    time.sleep(0.3)

    # Move focus to the back button.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Left'))
    time.sleep(0.3)

    # Press to return AppBar launcher page.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Move focus to the back button of AppBar launcher page.
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
        runTest(stub, CheckAppBarTestStart)
        runTest(stub, CheckAppBarTest11)
        runTest(stub, CheckAppBarTest12)
        runTest(stub, CheckAppBarTestEnd)


if __name__ == '__main__':                                         
    run()
