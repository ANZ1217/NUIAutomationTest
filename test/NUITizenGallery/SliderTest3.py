# test python script must be in same location as aurum_pb2.py

import grpc
from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import time
import argparse

isSliderTest3PageOpened = False
# XPos = 0
# YPos = 0


# Check if notification test1 page is opened or not.
def CheckSliderTest3Start(stub):
    LaunchAppTest(stub)

    global isSliderTest3PageOpened
    isSliderTest3PageOpened = FindTCByInputText(stub, "SliderTest3")
    time.sleep(0.3)
    return isSliderTest3PageOpened


# Check
def CheckSliderTest31(stub):
    if not isSliderTest3PageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType="Slider", isShowing=True))
    #print("==== : ", res)
    for slider in res.elements:
        if "slider1" in slider.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=slider.elementId))
            time.sleep(0.3)

            # geometry
            # {
            #     x: 240
            #     y: 230
            #     width: 1440
            #     height: 50
            # }
            XPos = slider.geometry.x
            YPos = slider.geometry.y

            stub.flick(ReqFlick(startPoint=Point(x=XPos, y=YPos), endPoint=Point(x=XPos + 170, y=YPos), durationMs=110))
            time.sleep(0.3)

            # Take ScreenShot.
            screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/Slider/SliderTest31.png")
            if screenShort is None:
                return False

            # Read image file expected.
            expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/Slider/SliderTest31.png')
            if expectedScreenShot is None:
                return False

            # Check ssim.
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckSliderTest32(stub):
    if not isSliderTest3PageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType="Slider", isShowing=True))
    for slider in res.elements:
        if "slider2" in slider.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=slider.elementId))
            time.sleep(0.3)

            # geometry
            # {
            #     x: 240
            #     y: 360
            #     width: 1440
            #     height: 50
            # }
            XPos = slider.geometry.x
            YPos = slider.geometry.y

            stub.flick(ReqFlick(startPoint=Point(x=XPos, y=YPos), endPoint=Point(x=XPos + 170, y=YPos), durationMs=110))
            time.sleep(0.3)

            # Take ScreenShot.
            screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/Slider/SliderTest32.png")
            if screenShort is None:
                return False

            # Read image file expected.
            expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/Slider/SliderTest32.png')
            if expectedScreenShot is None:
                return False

            # Check ssim.
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckSliderTest33(stub):
    if not isSliderTest3PageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType="Slider"))
    for slider in res.elements:
        if "slider3" in slider.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=slider.elementId))
            time.sleep(0.3)

            # geometry
            # {
            #     x: 860
            #     y: 490
            #     width: 50
            #     height: 360
            # }
            XPos = slider.geometry.x
            YPos = slider.geometry.y

            stub.flick(ReqFlick(startPoint=Point(x=XPos, y=YPos), endPoint=Point(x=XPos, y=YPos - 170), durationMs=110))
            time.sleep(0.3)

            # Take ScreenShot.
            screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/Slider/SliderTest33.png")
            if screenShort is None:
                return False

            # Read image file expected.
            expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/Slider/SliderTest33.png')
            if expectedScreenShot is None:
                return False

            # Check ssim.
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckSliderTest34(stub):
    if not isSliderTest3PageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType="Slider"))
    for slider in res.elements:
        if "slider4" in slider.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=slider.elementId))
            time.sleep(0.3)

            # geometry
            # {
            #     x: 1010
            #     y: 490
            #     width: 50
            #     height: 360
            # }
            XPos = slider.geometry.x
            YPos = slider.geometry.y

            stub.flick(ReqFlick(startPoint=Point(x=XPos, y=YPos), endPoint=Point(x=XPos, y=YPos - 100), durationMs=110))
            time.sleep(0.3)

            # Take ScreenShot.
            screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/Slider/SliderTest34.png")
            if screenShort is None:
                return False

            # Read image file expected.
            expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/Slider/SliderTest34.png')
            if expectedScreenShot is None:
                return False

            # Check ssim.
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckSliderTest35(stub):
    if not isSliderTest3PageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType="Slider", isShowing=True))
    for slider in res.elements:
        if "slider5" in slider.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=slider.elementId))
            time.sleep(0.3)

            # geometry
            # {
            #     x: 295
            #     y: 930
            #     width: 640
            #     height: 12
            # }
            XPos = slider.geometry.x
            YPos = slider.geometry.y

            stub.flick(ReqFlick(startPoint=Point(x=XPos, y=YPos), endPoint=Point(x=YPos, y=YPos), durationMs=110))
            time.sleep(0.3)

            # Take ScreenShot.
            screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/Slider/SliderTest35.png")
            if screenShort is None:
                return False

            # Read image file expected.
            expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/Slider/SliderTest35.png')
            if expectedScreenShot is None:
                return False

            # Check ssim.
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckSliderTest36(stub):
    if not isSliderTest3PageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType="Slider", isShowing=True))
    for slider in res.elements:
        if "slider6" in slider.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=slider.elementId))
            time.sleep(0.3)

            # geometry
            # {
            #     x: 985
            #     y: 930
            #     width: 640
            #     height: 12
            # }
            XPos = slider.geometry.x
            YPos = slider.geometry.y

            stub.flick(ReqFlick(startPoint=Point(x=XPos, y=YPos), endPoint=Point(x=XPos + 170, y=YPos), durationMs=110))
            time.sleep(0.3)
            stub.longClick(ReqClick(type="ELEMENTID", elementId=slider.elementId))
            time.sleep(0.3)

            # Take ScreenShot.
            screenShort = ReadScreenShotFile(stub, fileName="Results/TestedImages/Slider/SliderTest36.png")
            if screenShort is None:
                return False

            # Read image file expected.
            expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/Slider/SliderTest36.png')
            if expectedScreenShot is None:
                return False

            # Check ssim.
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckSliderTest3End(stub):
    global isSliderTest3PageOpened
    isSliderTest3PageOpened = False

    # Return to NUI Gallery page.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Exit Gallery.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='XF86Exit'))
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
        runTest(stub, CheckSliderTest3Start)
        runTest(stub, CheckSliderTest31)
        runTest(stub, CheckSliderTest32)
        runTest(stub, CheckSliderTest33)
        runTest(stub, CheckSliderTest34)
        runTest(stub, CheckSliderTest35)
        runTest(stub, CheckSliderTest36)
        runTest(stub, CheckSliderTest3End)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Options')
    parser.add_argument('--exit', dest='exit', action='store_true')
    parser.add_argument('--no-exit', dest='exit', action='store_false')
    parser.set_defaults(exit=True)
    args = parser.parse_args()
    run()
