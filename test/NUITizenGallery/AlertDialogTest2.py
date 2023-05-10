# test python script must be in same location as aurum_pb2.py

from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import grpc
import time
import argparse

isAlertDialogOpened = False

# Check if Alert Dialog is opened or not.
def CheckAlertDialogTestStart(stub):
    if not LaunchAppTest(stub):
        return False

    global isAlertDialogOpened
    isAlertDialogOpened = FindTCByInputText(stub, "AlertDialogTest2")
    time.sleep(0.3)
    return isAlertDialogOpened


# Check the first Dialog page.
def CheckAlertDialogTest21(stub):
    if isAlertDialogOpened == False:
        return False

    # Move focus to the button "Click to show Dialog".
    if(FindButtonandClickByText(stub, 'Click to show Dialog') == False):
        return False
    time.sleep(1)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/AlertDialog/AlertDialogTest21.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/AlertDialog/AlertDialogTest21.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check if AlertDialog exit normally.
def CheckAlertDialogTestEnd(stub):
    # Click Button 'Exit'.
    bts = stub.findElements(ReqFindElements(widgetType='Button', isShowing=True))
    for bt in bts.elements:
        if 'Exit' in bt.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=bt.elementId))
            stub.click(ReqClick(type="ELEMENTID", elementId=bt.elementId))
            time.sleep(0.3)

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
        runTest(stub, CheckAlertDialogTestStart)
        runTest(stub, CheckAlertDialogTest21)
        runTest(stub, CheckAlertDialogTestEnd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Options')
    parser.add_argument('--exit', dest='exit', action='store_true')
    parser.add_argument('--no-exit', dest='exit', action='store_false')
    parser.set_defaults(exit=True)
    args = parser.parse_args()
    run()
