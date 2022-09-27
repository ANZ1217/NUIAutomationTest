# test python script must be in same location as aurum_pb2.py

from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import grpc
import time
import argparse

isCollectionViewGridPageOpened = False

# Check if CollectionView grid page is opened or not.
def CheckCollectionViewGridTestStart(stub):
    if not LaunchAppTest(stub):
        return False

    global isCollectionViewGridPageOpened
    isCollectionViewGridPageOpened = FindTCByInputText(stub, "CollectionViewGridTest10")
    time.sleep(0.3)
    return isCollectionViewGridPageOpened


# Check if focus is moved horizontally.
def CheckCollectionViewGridTest101(stub):
    if isCollectionViewGridPageOpened == False:
        return False

    # Move focus to the fourth column of the first row.
    for i in range(4):
        stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Right'))
        time.sleep(0.3)

    # Select the image.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/CollectionView/CollectionViewTest101.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/CollectionView/CollectionViewTest101.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check if focus is moved vertically.
def CheckCollectionViewGridTest102(stub):
    if isCollectionViewGridPageOpened == False:
        return False

    # Move focus to the fourth column of the sixth row.
    for i in range(6):
        stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Down'))
        time.sleep(0.3)

    # Press button.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/CollectionView/CollectionViewTest102.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/CollectionView/CollectionViewTest102.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check if CollectionView exit normally.
def CheckCollectionViewGridTestEnd(stub):
    # Move focus to the back button.
    for i in range(8):
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
        runTest(stub, CheckCollectionViewGridTestStart)
        runTest(stub, CheckCollectionViewGridTest101)
        runTest(stub, CheckCollectionViewGridTest102)
        runTest(stub, CheckCollectionViewGridTestEnd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Options')
    parser.add_argument('--exit', dest='exit', action='store_true')
    parser.add_argument('--no-exit', dest='exit', action='store_false')
    parser.set_defaults(exit=True)
    args = parser.parse_args()
    run()
