# test python script must be in same location as aurum_pb2.py

import grpc
from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import time
import argparse

isNotificationPageOpened = False


# Check if notification test2 page is opened or not.
def CheckNotificationTestStart(stub):
    LaunchAppTest(stub)

    global isNotificationPageOpened
    isNotificationPageOpened = FindTCByInputText(stub, "NotificationTest2")
    time.sleep(0.3)
    return isNotificationPageOpened


# Check Dismiss after duration
def CheckNotificationTest3(stub):
    if not isNotificationPageOpened:
        return False

    # The notification should be dismissed after the specified duration
    time.sleep(4)

    # Take screenshot
    screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/Notification/NotificationTest3.png")
    if screenShort is None:
        return False

    # Read image file expected
    expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/Notification/NotificationTest3.png')
    if expectedScreenShot is None:
        return False

    # Check ssim
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check MakeToast
def CheckNotificationTest4(stub):
    if not isNotificationPageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button'))
    for elem in res.elements:
        if "MakeToast" in elem.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))
            time.sleep(1)

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/Notification/NotificationTest4.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/Notification/NotificationTest4.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckNotificationTestEnd(stub):
    global isNotificationPageOpened
    isNotificationPageOpened = False

    # Return to NUI Gallery page.
    ClickBackButton(stub)
    time.sleep(0.3)

    # Exit Gallery.
    ExitApp(stub)
    time.sleep(0.3)

    return True


def ReLaunch(stub):
    # Return to NUI Gallery page.
    ClickBackButton(stub)
    time.sleep(0.3)

    FindTCByInputText(stub, "NotificationTest2")
    return True


def runTest(stub, testFunc):
    print("Testing started :", testFunc.__name__)
    result = testFunc(stub)
    print("Testing {} result : {}".format(testFunc.__name__, result))

    return True


def run():
    with grpc.insecure_channel('localhost:50051', options=(('grpc.enable_http_proxy', 0),)) as channel:
        stub = BootstrapStub(channel)
        runTest(stub, CheckNotificationTestStart)
        runTest(stub, CheckNotificationTest3)
        runTest(stub, ReLaunch)
        runTest(stub, CheckNotificationTest4)
        # This sleep used to wait for the notification and toast to be disappeared
        time.sleep(2)
        runTest(stub, CheckNotificationTestEnd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Options')
    parser.add_argument('--exit', dest='exit', action='store_true')
    parser.add_argument('--no-exit', dest='exit', action='store_false')
    parser.set_defaults(exit=True)
    args = parser.parse_args()
    run()
