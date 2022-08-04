# test python script must be in same location as aurum_pb2.py

from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import grpc
import time

isCollectionViewLinearPageOpened = False

# Check if CollectionView page is opened or not.
def CheckCollectionViewLinearTestStart(stub):
    if not LaunchAppTest(stub):
        return False

    global isCollectionViewLinearPageOpened
    isCollectionViewLinearPageOpened = FindTCByInputText(stub, "CollectionViewLinearGroupTest12")
    time.sleep(0.3)
    return isCollectionViewLinearPageOpened


# Check if focus is moved vertically.
def CheckCollectionViewLinearTest121(stub):
    if isCollectionViewLinearPageOpened == False:
        return False

    # Move focus to the 14th row.
    for i in range(14):
        stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Down'))
        time.sleep(0.3)

    # Select the image.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="CollectionView/CollectionViewTest121.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='CollectionView/CollectionViewTestExpected121.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check if focus is moved vertically.
def CheckCollectionViewLinearTest122(stub):
    if isCollectionViewLinearPageOpened == False:
        return False

    # Move focus to the first row.
    for i in range(14):
        stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Up'))
        time.sleep(0.3)

    # Press button.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="CollectionView/CollectionViewTest122.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='CollectionView/CollectionViewTestExpected122.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check if CollectionView exit normally.
def CheckCollectionViewLinearTestEnd(stub):
    # Move focus to the back button.
    for i in range(3):
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
    with grpc.insecure_channel('localhost:50051') as channel:      
        stub = BootstrapStub(channel)
        runTest(stub, CheckCollectionViewLinearTestStart)
        runTest(stub, CheckCollectionViewLinearTest121)
        runTest(stub, CheckCollectionViewLinearTest122)
        runTest(stub, CheckCollectionViewLinearTestEnd)


if __name__ == '__main__':                                         
    run()
