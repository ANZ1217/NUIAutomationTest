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
    if(FindButtonandClickByText(stub, 'FPS++') == False):
        return False

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/Loading/LoadingTest11.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/Loading/LoadingTest11.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check the first loading.
def CheckLoadingTest12(stub):
    if not isLoadingPageOpened:
        return False

    # Move focus to the button "FPS++".
    if(FindButtonandClickByText(stub, 'FPS++') == False):
        return False

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/Loading/LoadingTest12.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/Loading/LoadingTest12.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check the second loading.
def CheckLoadingTest13(stub):
    if not isLoadingPageOpened:
        return False

    # Move focus to the button "Pause".
    if(FindButtonandClickByText(stub, 'Pause') == False):
        return False

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/Loading/LoadingTest13.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/Loading/LoadingTest13.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check if Loading exit normally.
def CheckLoadingTestEnd(stub):
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
