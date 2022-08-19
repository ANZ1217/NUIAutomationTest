# test python script must be in same location as aurum_pb2.py

import grpc
from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import time

isTimePickerPageOpened = False
XPos = 0
YPos = 0
Width = 0
Height = 0


# Check if switch test page is opened or not.
def CheckTimePickerTestStart(stub):
    if not LaunchAppTest(stub):
        return False

    global isTimePickerPageOpened
    isTimePickerPageOpened = FindTCByInputText(stub, "TimePickerTest1")
    time.sleep(1)
    return isTimePickerPageOpened


# Check Set
def CheckTimePickerTest1(stub):
    if not isTimePickerPageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button'))
    for elem in res.elements:
        if "Set" in elem.text:
            print("elem : ", elem)
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))
            time.sleep(1)

            GetGeometryInfo(stub)

            stub.flick(ReqFlick(startPoint=Point(x=XPos + int(Width / 7), y=YPos + int(Height / 6 * 4)),
                                endPoint=Point(x=XPos + int(Width / 7), y=YPos + int(Height / 6)), durationMs=110))
            time.sleep(0.3)

            stub.flick(ReqFlick(startPoint=Point(x=XPos + int(Width/2), y=YPos + int(Height / 6 * 4)),
                                endPoint=Point(x=XPos + int(Width/2), y=YPos + int(Height / 6)),durationMs=110))
            time.sleep(0.3)

            stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Down'))
            time.sleep(0.3)

            stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Down'))
            time.sleep(0.3)

            # Press button.
            stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
            time.sleep(0.3)

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="TimePicker/TimePickerTest01.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='TimePicker/TimePickerTestExpected01.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check Reset
def CheckTimePickerTest2(stub):
    if not isTimePickerPageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button'))
    for elem in res.elements:
        if "Reset" in elem.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))
            time.sleep(1)

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="TimePicker/TimePickerTest02.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='TimePicker/TimePickerTestExpected02.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckTimePickerTest3(stub):
    if not isTimePickerPageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button'))
    for elem in res.elements:
        if "Set" in elem.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))
            time.sleep(1)

            stub.flick(ReqFlick(startPoint=Point(x=XPos + int(Width / 7), y=YPos + int(Height / 6 * 4)),
                                endPoint=Point(x=XPos + int(Width / 7), y=YPos + int(Height / 6)), durationMs=110))
            time.sleep(0.3)

            stub.flick(ReqFlick(startPoint=Point(x=XPos + int(Width / 2), y=YPos + int(Height / 6 * 4)),
                                endPoint=Point(x=XPos + int(Width / 2), y=YPos + int(Height / 6)), durationMs=110))
            time.sleep(0.3)

            stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Down'))
            time.sleep(0.3)

            stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Down'))
            time.sleep(0.3)

            stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Right'))
            time.sleep(0.3)

            # Press button.
            stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
            time.sleep(0.3)

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="TimePicker/TimePickerTest03.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='TimePicker/TimePickerTestExpected03.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def GetGeometryInfo(stub):
    res = stub.findElements(ReqFindElements(widgetType='TimePicker'))
    for elem in res.elements:
        if "TimePicker" in elem.text:
            print("elem: ", elem)
        # geometry
        # {
        #     x: 660
        #     y: 361
        #     width: 600
        #     height: 339
        # }

        global XPos, YPos, Width, Height
        XPos = elem.geometry.x
        YPos = elem.geometry.y
        Width = elem.geometry.width
        Height = elem.geometry.height


def CheckTimePickerTestEnd(stub):
    global isTimePickerPageOpened
    isTimePickerPageOpened = False

    # Return to NUI Gallery page.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(1)

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
        time.sleep(1)
        runTest(stub, CheckTimePickerTestStart)
        runTest(stub, CheckTimePickerTest1)
        runTest(stub, CheckTimePickerTest2)
        runTest(stub, CheckTimePickerTest3)
        runTest(stub, CheckTimePickerTestEnd)


if __name__ == '__main__':
    run()
