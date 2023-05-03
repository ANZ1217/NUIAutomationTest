# test python script must be in same location as aurum_pb2.py

from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import grpc
import time
import argparse

isAppBarPageOpened = False

# Check if AppBar test page is opened or not.
def CheckAppBarTestStart(stub):
    if not LaunchAppTest(stub):
        return False

    global isAppBarPageOpened
    isAppBarPageOpened = FindTCByInputText(stub, "AppBarTest1")
    return isAppBarPageOpened


# Check the first AppBar page.
def CheckAppBarTest11(stub):
    if isAppBarPageOpened == False:
        return False

    # Click button "Click to show AppBar".
    response = stub.findElement(ReqFindElement(textField='Click to show AppBar'))
    if response.element is None:
        print("can not found button")
        return False

    targetObj = response.element.elementId

    stub.click(ReqClick(type='ELEMENTID', elementId=targetObj))

    time.sleep(1)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/AppBar/AppBarTest11.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/AppBar/AppBarTest11.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)

# Check the second AppBar page.
def CheckAppBarTest12(stub):
    if isAppBarPageOpened == False:
        return False

    #Click button "Click to next".
    response = stub.findElement(ReqFindElement(textField='Click to next'))
    if response.element is None:
        print("can not found button")
        return False

    targetObj = response.element.elementId
    stub.click(ReqClick(type='ELEMENTID', elementId=targetObj))
    time.sleep(1)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/AppBar/AppBarTest12.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/AppBar/AppBarTest12.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)

# Check if AppBar exit normally.
def CheckAppBarTestEnd(stub):

    #Click button "Pop page".
    response = stub.findElement(ReqFindElement(textField='Pop page'))
    if response.element is None:
        print("can not found button")
        return False

    targetObj = response.element.elementId
    stub.click(ReqClick(type='ELEMENTID', elementId=targetObj))
    time.sleep(1)

    #Click back button.
    stub.click(ReqClick(type='COORD', coordination=Point(x = 20, y = 20)))
    time.sleep(1)

    #Click back button.
    stub.click(ReqClick(type='COORD', coordination=Point(x = 20, y = 20)))
    time.sleep(1)

    # Exit Gallery.
    stub.closeApp(ReqCloseApp(packageName='org.tizen.example.NUITizenGallery'))
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
        runTest(stub, CheckAppBarTestStart)
        runTest(stub, CheckAppBarTest11)
        runTest(stub, CheckAppBarTest12)
        runTest(stub, CheckAppBarTestEnd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Options')
    parser.add_argument('--exit', dest='exit', action='store_true')
    parser.add_argument('--no-exit', dest='exit', action='store_false')
    parser.set_defaults(exit=True)
    args = parser.parse_args()
    run()
