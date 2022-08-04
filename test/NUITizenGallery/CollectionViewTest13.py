# test python script must be in same location as aurum_pb2.py

from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import grpc
import time

isCollectionViewGridGroupPageOpened = False

# Check if CollectionView grid page is opened or not.
def CheckCollectionViewGridGroupTestStart(stub):
    if not LaunchAppTest(stub):
        return False

    global isCollectionViewGridGroupPageOpened
    isCollectionViewGridGroupPageOpened = FindTCByInputText(stub, "CollectionViewGridGroupTest13")
    time.sleep(0.3)
    return isCollectionViewGridGroupPageOpened


# Check if focus is moved vertically.
def CheckCollectionViewGridGroupTest131(stub):
    if isCollectionViewGridGroupPageOpened == False:
        return False

    # Move focus to the fourth column of the first row.
    for i in range(6):
        stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Down'))
        time.sleep(0.3)

    # Select the image.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="CollectionView/CollectionViewTest131.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='CollectionView/CollectionViewTestExpected131.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check if focus is moved horizontally.
def CheckCollectionViewGridGroupTest132(stub):
    if isCollectionViewGridGroupPageOpened == False:
        return False

    # Move focus to the fourth column of the sixth row.
    for i in range(6):
        stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Right'))
        time.sleep(0.3)

    # Press button.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="CollectionView/CollectionViewTest132.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='CollectionView/CollectionViewTestExpected132.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check if CollectionView exit normally.
def CheckCollectionViewGridGroupTestEnd(stub):
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
    with grpc.insecure_channel('localhost:50051') as channel:      
        stub = BootstrapStub(channel)
        runTest(stub, CheckCollectionViewGridGroupTestStart)
        runTest(stub, CheckCollectionViewGridGroupTest131)
        runTest(stub, CheckCollectionViewGridGroupTest132)
        runTest(stub, CheckCollectionViewGridGroupTestEnd)


if __name__ == '__main__':                                         
    run()
