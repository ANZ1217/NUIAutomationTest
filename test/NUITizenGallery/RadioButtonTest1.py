# test python script must be in same location as aurum_pb2.py

import grpc
from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import time
import argparse

isRadioButtonPageOpened = False


# Check if notification test1 page is opened or not.
def CheckRadioButtonTestStart(stub):
    LaunchAppTest(stub)

    global isRadioButtonPageOpened
    isRadioButtonPageOpened = FindTCByInputText(stub, "RadioButtonTest1")
    time.sleep(0.3)
    return isRadioButtonPageOpened


# Check
def CheckRadioButton1(stub):
    if not isRadioButtonPageOpened:
        return False

    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Down'))
    time.sleep(0.3)

    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Right'))
    time.sleep(0.3)

    # Press TabButton.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Take ScreenShot.
    screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/RadioButton/RadioButtonTest1.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/RadioButton/RadioButtonTest1.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckRadioButtonTestEnd(stub):
    global isRadioButtonPageOpened
    isRadioButtonPageOpened = False

    # Return to NUI Gallery page.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Exit Gallery.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='XF86Exit'))
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
        runTest(stub, CheckRadioButtonTestStart)
        runTest(stub, CheckRadioButton1)
        runTest(stub, CheckRadioButtonTestEnd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Options')
    parser.add_argument('--exit', dest='exit', action='store_true')
    parser.add_argument('--no-exit', dest='exit', action='store_false')
    parser.set_defaults(exit=True)
    args = parser.parse_args()
    run()
