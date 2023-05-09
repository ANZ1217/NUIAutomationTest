# test python script must be in same location as aurum_pb2.py

from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import grpc
import time
import argparse

isDialogPageOpened = False

# Check if Dialog page is opened or not.
def CheckDialogPageTestStart(stub):
    if not LaunchAppTest(stub):
        return False

    global isDialogPageOpened
    isDialogPageOpened = FindTCByInputText(stub, "DialogPageTest")
    time.sleep(0.3)
    return isDialogPageOpened


# Check the first Dialog page.
def CheckDialogPageTest1(stub):
    if isDialogPageOpened == False:
        return False

    # Click button "Click to show Dialog".
    if(FindButtonandClickByText(stub, 'Click to show Dialog') == False):
        return False

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/DialogPage/DialogPageTest01.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/DialogPage/DialogPageTest01.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check if DialogPage exit normally.
def CheckDialogPageTestEnd(stub):
    # Click textlabel 'Message'.
    tls = stub.findElements(ReqFindElements(widgetType='TextLabel', isShowing=True))
    for tl in tls.elements:
        if 'Message' in tl.text:
            stub.click(ReqClick(coordination=Point(x=200,y=200), type='COORD'))
            time.sleep(0.3)

    #Click back button.
    ClickBackButton(stub)
    time.sleep(1)

    return True


def runTest(stub, testFunc):
    print("Testing started :", testFunc.__name__)
    result = testFunc(stub)
    print("Testing {} result : {}".format(testFunc.__name__, result))

    return True


def run():
    with grpc.insecure_channel('localhost:50051', options=(('grpc.enable_http_proxy', 0),)) as channel:
        stub = BootstrapStub(channel)
        runTest(stub, CheckDialogPageTestStart)
        runTest(stub, CheckDialogPageTest1)
        runTest(stub, CheckDialogPageTestEnd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Options')
    parser.add_argument('--exit', dest='exit', action='store_true')
    parser.add_argument('--no-exit', dest='exit', action='store_false')
    parser.set_defaults(exit=True)
    args = parser.parse_args()
    run()
