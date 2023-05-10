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

    # Press button.
    if(FindButtonandClickByText(stub, 'Button') == False):
        return False
    time.sleep(1)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/Button/ButtonTest81.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/Button/ButtonTest81.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check the second button.
def CheckButtonTest82(stub):
    if isButtonPageOpened == False:
        return False

    # Press button.
    FindButtonandClickByGeometry(stub, 250, 64, 80, 80)
    time.sleep(1)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/Button/ButtonTest82.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/Button/ButtonTest82.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check the third button.
def CheckButtonTest83(stub):
    if isButtonPageOpened == False:
        return False

    # Press button.
    FindButtonandClickByGeometry(stub, 250, 194, 80, 80)
    time.sleep(1)

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/Button/ButtonTest83.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check the fourth button.
def CheckButtonTest84(stub):
    if isButtonPageOpened == False:
        return False

    # Move focus to the fourth button.
    if(FindButtonandClickByText(stub, 'IconTextButton') == False):
        return False
    time.sleep(1)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/Button/ButtonTest84.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/Button/ButtonTest84.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check if Button page exit normally.
def CheckButtonTestEnd(stub):

    # Press to NUI Gallery page.
    ClickBackButton(stub)
    time.sleep(0.3)

    # Exit Gallery.
    ExitApp(stub)
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
