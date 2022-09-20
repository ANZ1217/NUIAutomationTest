# test python script must be in same location as aurum_pb2.py

import grpc
from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import time
import argparse

isSliderTest4PageOpened = False


# Check if notification test1 page is opened or not.
def CheckSliderTest4Start(stub):
    LaunchAppTest(stub)

    global isSliderTest4PageOpened
    isSliderTest4PageOpened = FindTCByInputText(stub, "SliderTest4")
    time.sleep(0.3)
    return isSliderTest4PageOpened


# Check
def CheckSliderTest41(stub):
    if not isSliderTest4PageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType="Slider"))
    for slider in res.elements:
        if "slider41" in slider.text:
            print("====== slider41 =======:", slider)
            stub.click(ReqClick(type="ELEMENTID", elementId=slider.elementId))
            time.sleep(0.3)

            # geometry
            # {
            #     x: 480
            #     y: 446
            #     width: 960
            #     height: 20
            # }
            XPos = slider.geometry.x
            YPos = slider.geometry.y

            stub.flick(ReqFlick(startPoint=Point(x=XPos, y=YPos), endPoint=Point(x=XPos, y=YPos - 190), durationMs=110))
            time.sleep(0.3)

            # Take ScreenShot.
            screenShort = ReadScreenShotFile(stub, fileName="Slider/SliderTest41.png")
            if screenShort is None:
                return False

            # Read image file expected.
            expectedScreenShot = ReadImageFile(fileName='Slider/SliderTestExpected41.png')
            if expectedScreenShot is None:
                return False

            # Check ssim.
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckSliderTest42(stub):
    if not isSliderTest4PageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType="Slider"))
    for slider in res.elements:
        if "slider42" in slider.text:
            print("====== slider42 =======:", slider)
            stub.click(ReqClick(type="ELEMENTID", elementId=slider.elementId))
            time.sleep(0.3)

            # geometry
            # {
            #     x: 480
            #     y: 642
            #     width: 960
            #     height: 20
            # }
            XPos = slider.geometry.x
            YPos = slider.geometry.y

            stub.flick(ReqFlick(startPoint=Point(x=XPos, y=YPos), endPoint=Point(x=XPos, y=YPos - 170), durationMs=110))
            time.sleep(0.3)

            # Take ScreenShot.
            screenShort = ReadScreenShotFile(stub, fileName="Slider/SliderTest42.png")
            if screenShort is None:
                return False

            # Read image file expected.
            expectedScreenShot = ReadImageFile(fileName='Slider/SliderTestExpected42.png')
            if expectedScreenShot is None:
                return False

            # Check ssim.
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckSliderTest43(stub):
    if not isSliderTest4PageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType="Slider"))
    for slider in res.elements:
        if "slider43" in slider.text:
            print("====== slider43 =======:", slider)
            stub.click(ReqClick(type="ELEMENTID", elementId=slider.elementId))
            time.sleep(0.3)

            # geometry
            # {
            #     x: 480
            #     y: 838
            #     width: 960
            #     height: 20
            # }
            XPos = slider.geometry.x
            YPos = slider.geometry.y

            stub.flick(ReqFlick(startPoint=Point(x=XPos, y=YPos), endPoint=Point(x=XPos, y=YPos - 150), durationMs=110))
            time.sleep(0.3)

            # Take ScreenShot.
            screenShort = ReadScreenShotFile(stub, fileName="Slider/SliderTest43.png")
            if screenShort is None:
                return False

            # Read image file expected.
            expectedScreenShot = ReadImageFile(fileName='Slider/SliderTestExpected43.png')
            if expectedScreenShot is None:
                return False

            # Check ssim.
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckSliderTest4End(stub):
    global isSliderTest4PageOpened
    isSliderTest4PageOpened = False

    # Return to NUI Gallery page.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Exit Gallery.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='XF86Exit'))
    time.sleep(0.3)
    return True


def runTest(stub, testFunc):
    print("Testing started :", testFunc)
    result = testFunc(stub)
    print("Testing result :", result)
    return True


def run():
    with grpc.insecure_channel('localhost:50051', options=(('grpc.enable_http_proxy', 0),)) as channel:
        stub = BootstrapStub(channel)
        runTest(stub, CheckSliderTest4Start)
        runTest(stub, CheckSliderTest41)
        runTest(stub, CheckSliderTest42)
        runTest(stub, CheckSliderTest43)
        runTest(stub, CheckSliderTest4End)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Options')
    parser.add_argument('--exit', dest='exit', action='store_true')
    parser.add_argument('--no-exit', dest='exit', action='store_false')
    parser.set_defaults(exit=True)
    args = parser.parse_args()
    run()
