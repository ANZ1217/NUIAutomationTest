# test python script must be in same location as aurum_pb2.py

from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import grpc
import time
import argparse

isWidgetViewOpened = False

# Launch application. it returns application running state
def CheckWidgetViewTestStart(stub):
    if not LaunchAppTest(stub):
        return False

    global isWidgetViewOpened
    isWidgetViewOpened = FindTCByInputText(stub, "WidgetViewTest1")
    time.sleep(2)
    return isWidgetViewOpened


# Check '1' key.
def CheckWidgetViewTest11(stub):
    if not isWidgetViewOpened:
        return False

    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='1'))
    time.sleep(1)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/WidgetView/WidgetViewTest11.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/WidgetView/WidgetViewTest11.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check if WidgetView exit normally.
def CheckWidgetViewTestEnd(stub):
    # Exit.
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
        runTest(stub, CheckWidgetViewTestStart)
        runTest(stub, CheckWidgetViewTest11)
        runTest(stub, CheckWidgetViewTestEnd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Options')
    parser.add_argument('--exit', dest='exit', action='store_true')
    parser.add_argument('--no-exit', dest='exit', action='store_false')
    parser.set_defaults(exit=True)
    args = parser.parse_args()
    run()
