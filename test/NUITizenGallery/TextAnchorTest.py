from __future__ import print_function
from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
import logging
import grpc
import time
import argparse

# Check the object in the screen(TM1) or not
def inScreen(size):
    if size.x < 0: return False
    if size.y < 0: return False
    if size.x >= 720: return False
    if size.y >= 1280: return False
    return True

# 1. Find TextField(entry)
# 2. Set Text as Anchor
# 3. Click Run button
# 4. Find TextAnchorTest item on the result list
# 5. Find 'Text Anchor Test' textlabel on the layout
def AnchorExecuteTestWithText(stub):
    # 1
    response = stub.findElement(ReqFindElement(widgetType='TextField'))
    if len(response.elements) <= 0: return False
    # 2
    targetObj = response.elements[0].elementId
    testString = 'Anchor'
    stub.setValue(ReqSetValue(elementId=targetObj, stringValue=testString))
    # 3
    response = stub.findElement(ReqFindElement(textField='Run'))
    if len(response.elements) <= 0: return False
    targetObj = response.elements[0].elementId
    stub.click(ReqClick(type='ELEMENTID', elementId=targetObj))
    # 4
    response = stub.findElement(ReqFindElement(textField='TextAnchorTest'))
    if len(response.elements) <= 0: return False
    targetObj = response.elements[0].elementId
    stub.click(ReqClick(type='ELEMENTID', elementId=targetObj))
    # 5
    response = stub.findElement(ReqFindElement(textField='Text Anchor Test'))
    if len(response.elements) <= 0: return False

    return True

# 1. Find 'Click TextLabel Anchor' textlabel
# 2. Get textlabel geometry value for click event
# 3. Click textlabel anchor
# 4. Find 'www.tizen.org/TextLabel' textfield on the layout
def LabelAnchorClickTest(stub):
    # 1
    response = stub.findElement(ReqFindElement(textField='Click TextLabel Anchor'))
    if len(response.elements) <= 0: return False

    # 2
    anchorX = response.elements[0].geometry.x + 10
    anchorY = response.elements[0].geometry.y + 10

    # 3
    stub.click(ReqClick(type='COORD', coordination=Point(x=anchorX, y=anchorY)))

    # 4
    response = stub.findElement(ReqFindElement(textField='www.tizen.org/TextLabel'))
    if len(response.elements) <= 0: return False

    return True

# 1. Find 'Click TextField Anchor' textlabel
# 2. Get textfield geometry value for click event
# 3. Click textfield anchor
# 4. Find 'www.tizen.org/TextField' textfield on the layout
def FieldAnchorClickTest(stub):
    # 1
    response = stub.findElement(ReqFindElement(textField='Click TextField Anchor'))
    if len(response.elements) <= 0: return False

    # 2
    anchorX = response.elements[0].geometry.x + 10
    anchorY = response.elements[0].geometry.y + 10

    # 3
    stub.click(ReqClick(type='COORD', coordination=Point(x=anchorX, y=anchorY)))

    # 4
    response = stub.findElement(ReqFindElement(textField='www.tizen.org/TextField'))
    if len(response.elements) <= 0: return False

    return True

# 1. Find 'Click TextEditor Anchor' textlabel
# 2. Get texteditor geometry value for click event
# 3. Click texteditor anchor
# 4. Find 'www.tizen.org/TextEditor' textfield on the layout
def EditorAnchorClickTest(stub):
    # 1
    response = stub.findElement(ReqFindElement(textField='Click TextEditor Anchor'))
    if len(response.elements) <= 0: return False

    # 2
    anchorX = response.elements[0].geometry.x + 10
    anchorY = response.elements[0].geometry.y + 10

    # 3
    stub.click(ReqClick(type='COORD', coordination=Point(x=anchorX, y=anchorY)))

    # 4
    response = stub.findElement(ReqFindElement(textField='www.tizen.org/TextEditor'))
    if len(response.elements) <= 0: return False

    return True

# Launch application. it returns application running state
def launchAppTest(stub):
    stub.launchApp(ReqLaunchApp(packageName='org.tizen.example.NUITizenGallery'))
    return stub.getAppInfo(ReqGetAppInfo(packageName='org.tizen.example.NUITizenGallery')).isRunning

# Close application. it returns application running state
def closeAppTest(stub):
    stub.closeApp(ReqCloseApp(packageName='org.tizen.example.NUITizenGallery'))
    return stub.getAppInfo(ReqGetAppInfo(packageName='org.tizen.example.NUITizenGallery')).isRunning != True

def defaultSetup(stub):
    if stub.getAppInfo(ReqGetAppInfo(packageName='org.tizen.example.NUITizenGallery')).isRunning:
        stub.closeApp(ReqCloseApp(packageName='org.tizen.example.NUITizenGallery'))

    stub.launchApp(ReqLaunchApp(packageName='org.tizen.example.NUITizenGallery'))

def defaultTearDown(stub):
    stub.closeApp(ReqCloseApp(packageName='org.tizen.example.NUITizenGallery'))

def runTest(stub, testFunc, setup=defaultSetup, tearDown=defaultTearDown, alwaySucceed=False):
    print("Testing started :", testFunc)

    setup(stub)
    result = testFunc(stub)
    tearDown(stub)

    print("Testing result :", result)
    if alwaySucceed: return True

def runTestWithoutSetupAndTearDown(stub, testFunc, setup=defaultSetup, tearDown=defaultTearDown):
    def Empty(stub):
        pass

    runTest(stub, testFunc, Empty, Empty)

def run():
    with grpc.insecure_channel('127.0.0.1:50051') as channel:
        stub = BootstrapStub(channel)
        # Anchor Test
        runTestWithoutSetupAndTearDown(stub, launchAppTest)
        runTestWithoutSetupAndTearDown(stub, AnchorExecuteTestWithText)
        runTestWithoutSetupAndTearDown(stub, LabelAnchorClickTest)
        runTestWithoutSetupAndTearDown(stub, FieldAnchorClickTest)
        runTestWithoutSetupAndTearDown(stub, EditorAnchorClickTest)
        runTestWithoutSetupAndTearDown(stub, closeAppTest)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Options')
    parser.add_argument('--exit', dest='exit', action='store_true')
    parser.add_argument('--no-exit', dest='exit', action='store_false')
    parser.set_defaults(exit=True)
    args = parser.parse_args()
    logging.basicConfig()
    run()
