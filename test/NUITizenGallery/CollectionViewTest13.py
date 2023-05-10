# test python script must be in same location as aurum_pb2.py

from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import grpc
import time
import argparse

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

    time.sleep(1)

    # Move focus to the fourth column of the first row.
    stub.flick(ReqFlick(startPoint=Point(x=160, y=250), endPoint=Point(x=160, y=130), durationMs=110))
    time.sleep(8)

    if(FindButtonandClickByText(stub, '[6] : Statue') == False):
        return False
    time.sleep(1)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/CollectionView/CollectionViewTest131.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/CollectionView/CollectionViewTest131.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check if focus is moved horizontally.
def CheckCollectionViewGridGroupTest132(stub):
    if isCollectionViewGridGroupPageOpened == False:
        return False

    # Move focus to the fourth column of the sixth row.
    if(FindButtonandClickByText(stub, '[11] : Icicle') == False):
        return False
    time.sleep(1)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/CollectionView/CollectionViewTest132.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/CollectionView/CollectionViewTest132.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check if CollectionView exit normally.
def CheckCollectionViewGridGroupTestEnd(stub):

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
        runTest(stub, CheckCollectionViewGridGroupTestStart)
        runTest(stub, CheckCollectionViewGridGroupTest131)
        runTest(stub, CheckCollectionViewGridGroupTest132)
        runTest(stub, CheckCollectionViewGridGroupTestEnd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Options')
    parser.add_argument('--exit', dest='exit', action='store_true')
    parser.add_argument('--no-exit', dest='exit', action='store_false')
    parser.set_defaults(exit=True)
    args = parser.parse_args()
    run()
