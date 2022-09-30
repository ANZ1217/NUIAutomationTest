# test python script must be in same location as aurum_pb2.py

from aurum_pb2 import *
import grpc
import cv2
import numpy as np
import os
import sys
import time

# Launch application. it returns application running state
def LaunchAppTest(stub):
    if stub.getAppInfo(ReqGetAppInfo(packageName='org.tizen.example.NUITizenGallery')).isRunning:
        stub.closeApp(ReqCloseApp(packageName='org.tizen.example.NUITizenGallery'))
        time.sleep(1)

    stub.launchApp(ReqLaunchApp(packageName='org.tizen.example.NUITizenGallery'))
    # This sleep is needed, or ReqFindElement will report "Status: Error" during do all test
    time.sleep(5)
    return stub.getAppInfo(ReqGetAppInfo(packageName='org.tizen.example.NUITizenGallery')).isRunning


def FindTCByInputText(stub, targetTC):
    response = stub.findElement(ReqFindElement(widgetType='TextField'))
    if response.element is None:
        #print("can not find TextField")
        return False

    targetObj = response.element.elementId
    stub.setValue(ReqSetValue(elementId=targetObj, stringValue=targetTC))

    response = stub.findElement(ReqFindElement(textField='Run'))
    if response.element is None:
        #print("can not found Run button")
        return False

    targetObj = response.element.elementId
    stub.click(ReqClick(type='ELEMENTID', elementId=targetObj))

    response = stub.findElements(ReqFindElements(textPartialMatch=targetTC))
    if len(response.elements) < 2:
        return False

    targetObj = response.elements[1].elementId

    res = stub.click(ReqClick(type='ELEMENTID', elementId=targetObj))
    return True


def FindTCAndClickByFlicking(stub, targetTC):
    stub.launchApp(ReqLaunchApp(packageName="org.tizen.example.NUITizenGallery"))
    time.sleep(5)

    isRunning = stub.getAppInfo(ReqGetAppInfo(packageName="org.tizen.example.NUITizenGallery")).isRunning
    #print("isRunning=", isRunning)
    time.sleep(1)

    for tryCnt in range(9):
        #print('FindTCAndClickByFlicking() @ tries:', tryCnt)
        res = stub.findElements(ReqFindElements(widgetType='DefaultLinearItem', isShowing=True))
        for tc in res.elements:
            if targetTC in tc.text:
                #print("found target TC:", tc.text)
                time.sleep(3)
                stub.click(ReqClick(type="ELEMENTID", elementId=tc.elementId))
                return True

        stub.flick(ReqFlick(startPoint=Point(x=160, y=459), endPoint=Point(x=160, y=130), durationMs=110))
        time.sleep(3)

    ㅍ("couldn't found target TC:", targetTC)
    return False


def ReadImageFile(fileName):
    # Get current dir
    currentDir = os.path.dirname(os.path.abspath(__file__))
    #print('current dir is ', currentDir)

    # Check if file exists.
    path = currentDir + '/' + fileName
    if not os.path.isfile(path):
        return None

    return cv2.imread(path)


def ReadScreenShotFile(stub, fileName):
    # Get current dir
    currentDir = os.path.dirname(os.path.abspath(__file__))
    #print('current dir is ', currentDir)

    # Create dir if neccessary.
    path = currentDir + '/' + fileName
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Take screen shot.
    #print("take a screen shot")
    image = open(path, "wb")
    time.sleep(1)
    screenShot = stub.takeScreenshot(ReqTakeScreenshot())
    for sshot in screenShot:
        image.write(sshot.image)
    image.close()
    #print("File written!")

    return cv2.imread(path)


def CheckSSIM(answerImge, testTargetImage):
    # Preliminary computing
    I1 = answerImge.astype(float)
    I2 = testTargetImage.astype(float)

    I2_2 = np.multiply(I2, I2)
    I1_2 = np.multiply(I1, I1)
    I1_I2 = np.multiply(I1, I2)

    mu1 = cv2.GaussianBlur(I1, (11,11), 1.5)
    mu2 = cv2.GaussianBlur(I2, (11,11), 1.5)

    mu1_2 = np.multiply(mu1, mu1)
    mu2_2 = np.multiply(mu2, mu2)
    mu1_mu2 = np.multiply(mu1, mu2)

    sigma1_2 = cv2.GaussianBlur(I1_2, (11,11), 1.5)
    sigma1_2 = np.subtract(sigma1_2, mu1_2)

    sigma2_2 = cv2.GaussianBlur(I2_2, (11,11), 1.5)
    sigma2_2 = np.subtract(sigma2_2, mu2_2)

    sigma12 = cv2.GaussianBlur(I1_I2, (11,11), 1.5)
    sigma12 = np.subtract(sigma12, mu1_mu2)

    # Formulate
    C1 = 0.01 * 255 * 0.01 * 255
    C2 = 0.03 * 255 * 0.03 * 255

    t1 = np.add(np.multiply(2, mu1_mu2), C1)
    t2 = np.add(np.multiply(2, sigma12), C2)
    t3 = np.multiply(t1, t2)

    t1 = np.add(np.add(mu1_2, mu2_2), C1)
    t2 = np.add(np.add(sigma1_2, sigma2_2), C2)
    t1 = np.multiply(t1, t2)

    ssim_map = np.divide(t3, t1)
    ssim_map = np.mean(ssim_map)
    #print("ssim value is ", ssim_map)
    return ssim_map >= 0.99
