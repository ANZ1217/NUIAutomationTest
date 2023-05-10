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
    if(FindButtonandClickByText(stub, '[10] : Inserted Item') == False):
        return False
    time.sleep(1)

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
    stub.flick(ReqFlick(startPoint=Point(x=160, y=400), endPoint=Point(x=160, y=130), durationMs=110))
    time.sleep(5)

    if(FindButtonandClickByText(stub, '[29] : Police') == False):
        return False
    time.sleep(1)

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

    # Press to NUI Gallery page.
    ClickBackButton(stub)

    # Exit Gallery.
    ExitApp(stub)
    return True


def runTest(stub, testFunc):
    print("Testing started :", testFunc.__name__)
    result = testFunc(stub)
    print("Testing {} result : {}".format(testFunc.__name__, result))

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
