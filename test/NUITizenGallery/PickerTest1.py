from __future__ import print_function
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.dirname(__file__)))))
from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
import logging
import grpc
import time
import argparse
from NUIGalleryTestUtils import *

def inScreen(size):
    if size.x < 0: return False
    if size.y < 0: return False
    if size.x >= 1920: return False
    if size.y >= 1080: return False
    return True

def PickerExecuteTestWithText(stub):
    response = stub.findElement(ReqFindElement(widgetType='TextField'))
    if response.element is None:
        print("can not find TextField")
        return False

    targetObj = response.element.elementId
    testString = 'Picker'
    stub.setValue(ReqSetValue(elementId=targetObj, stringValue=testString))

    response = stub.findElement(ReqFindElement(textField='Run'))
    if response.element is None:
        print("can not found Run button")
        return False

    targetObj = response.element.elementId
    stub.click(ReqClick(type='ELEMENTID', elementId=targetObj))

    response = stub.findElement(ReqFindElement(textField='PickerTest1, '))
    if response.element is None:
        return False
    targetObj = response.element.elementId
    res = stub.click(ReqClick(type='ELEMENTID', elementId=targetObj))

    response = stub.findElements(ReqFindElements(textField='Black'))
    if len(response.elements) <= 0:
        print("can not find black")
        return False

    screenShot = ReadScreenShotFile(stub, fileName="Results/TestedImages/Picker/PickerTest11.png")
    if screenShot is None:
        return False

    expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/Picker/PickerTest11.png')
    if expectedScreenShot is None:
        return False

    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShot)


def PickerExecuteTest(stub):
    for tryCnt in range(10):
        stub.flick(ReqFlick(startPoint=Point(x=300, y=750), endPoint=Point(x=300, y=200), durationMs=150))
        response = stub.findElement(ReqFindElement(textField='PickerTest1'))
        if response.elements is None: continue
        targetObj = response.element.elementId
        response = stub.getSize(ReqGetSize(elementId=targetObj))
        if inScreen(response.size):
            stub.click(ReqClick(type='ELEMENTID', elementId=targetObj))
            break

    response = stub.findElements(ReqFindElements(textField='Black'))
    if len(response.elements) <= 0: return False
    return True

def PickerScrollTest(stub):
    response = stub.findElements(ReqFindElements(widgetType='PickerScroller'))
    if len(response.elements) <= 0: return False

    responseText = stub.findElements(ReqFindElements(textPartialMatch='Black'))
    if responseText.elements is None:
        print("can not find Black")
        return False

    pickerCenterY = 0

    for e in responseText.elements:
        if e.geometry.y > pickerCenterY:
            response = e

    pickerCenterX = response.geometry.x + (response.geometry.width / 2)
    pickerCenterY = response.geometry.y + (response.geometry.height / 2)

    for tryCnt in range(30):
        stub.flick(ReqFlick(startPoint=Point(x=int(pickerCenterX), y=int(pickerCenterY)), endPoint=Point(x=int(pickerCenterX), y=int(pickerCenterY-70)), durationMs=100))
        time.sleep(0.2)
        response = stub.findElement(ReqFindElement(textField='Yellow'))
        if response.element:
            if tryCnt > 3:
                screenShot = ReadScreenShotFile(stub, fileName="Results/TestedImages/Picker/PickerTest12.png")
                if screenShot is None:
                    return False
                expectedScreenShot = ReadImageFile(fileName='Results/ExpectedImages/Picker/PickerTest12.png')
                if expectedScreenShot is None:
                    return False
                return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShot)

    return False

def launchAppTest(stub):
    stub.launchApp(ReqLaunchApp(packageName='org.tizen.example.NUITizenGallery'))
    return stub.getAppInfo(ReqGetAppInfo(packageName='org.tizen.example.NUITizenGallery')).isRunning

def closeAppTest(stub):
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Up'))
    time.sleep(0.3)

    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Up'))
    time.sleep(0.3)

    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)
    return True

def defaultSetup(stub):
    if stub.getAppInfo(ReqGetAppInfo(packageName='org.tizen.example.NUITizenGallery')).isRunning:
        stub.closeApp(ReqCloseApp(packageName='org.tizen.example.NUITizenGallery'))

    stub.launchApp(ReqLaunchApp(packageName='org.tizen.example.NUITizenGallery'))

def defaultTearDown(stub):
    stub.closeApp(ReqCloseApp(packageName='org.tizen.example.NUITizenGallery'))

def runTest(stub, testFunc, setup=defaultSetup, tearDown=defaultTearDown, alwaySucceed=False):
    print("Testing started :", testFunc.__name__)

    setup(stub)
    result = testFunc(stub)
    tearDown(stub)

    print("Testing {} result : {}".format(testFunc.__name__, result))

    if alwaySucceed: return True

def runTestWithoutSetupAndTearDown(stub, testFunc, setup=defaultSetup, tearDown=defaultTearDown):
    def Empty(stub):
        pass

    runTest(stub, testFunc, Empty, Empty)

def run():
    with grpc.insecure_channel('localhost:50051', options=(('grpc.enable_http_proxy', 0),)) as channel:
        stub = BootstrapStub(channel)

        runTestWithoutSetupAndTearDown(stub, launchAppTest)
        runTestWithoutSetupAndTearDown(stub, PickerExecuteTestWithText)
        runTestWithoutSetupAndTearDown(stub, PickerScrollTest)
        runTestWithoutSetupAndTearDown(stub, closeAppTest)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Options')
    parser.add_argument('--exit', dest='exit', action='store_true')
    parser.add_argument('--no-exit', dest='exit', action='store_false')
    parser.set_defaults(exit=True)
    args = parser.parse_args()
    logging.basicConfig()
    run()
