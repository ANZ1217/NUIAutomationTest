# test python script must be in same location as aurum_pb2.py

import glob
import os
import re
import shutil
import subprocess
import datetime
import argparse

# Testcases list.
def GetTCList():
    with open('./tclist.txt') as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        return lines


def RemoveAllDirs(tcFileNameList, target):
    for item in tcFileNameList:
        print("================{}=======================".format(item))
        r = re.compile("([a-zA-Z]+)Test([0-9]*)")
        m = r.match(item)
        dirName = m.group(1)
        path1 = './Results/ExpectedImages/{}'.format(dirName)
        if os.path.isdir(path1):
            shutil.rmtree(path1)  # remove dir and all contains
            print('Directory {} is removed.'.format(path1))
        path2 = './ExpectedImages/{}/{}.format(target, dirName)'
        if os.path.isdir(path2):
            shutil.rmtree(path2)  # remove dir and all contains
            print('Directory {} is removed.'.format(path2))


def RunTest(pyFileName):
    python_version = '3'
    path_to_run = './'
    py_name = pyFileName + '.py'

    args = ["python{}".format(python_version), "{}{}".format(path_to_run, py_name)]
    proc = subprocess.Popen(args, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        output, error_ = proc.communicate(timeout=120)
    except subprocess.TimeoutExpired:
        proc.kill()
        output, error_ = proc.communicate()

    if error_:
        print(error_)
        return False

    return True


def RenameImageFileNames(target):
    passedCount = 0
    failedCount = 0
    tcFileNameList = GetTCList()

    print("{} Screenshot will be generated".format(target))

    # Remove all directories.
    RemoveAllDirs(tcFileNameList, target)

    # Generate screenshots expected.
    for item in tcFileNameList:
        now = datetime.datetime.now()
        print("================{}============== {}:{}:{}".format(item, now.hour, now.minute, now.second))

        ret = RunTest(item)
        if ret:
            #r = re.compile("([a-zA-Z]+)Test([0-9]+)")
            m = re.match("([a-zA-Z]+)Test([0-9]+)", item)
            dirName = m.group(1)
            #print(dirName)
            imageList = glob.glob("./Results/TestedImages/*")
            for testPath in imageList:
                print("{} copying".format(testPath))
                destPath = "./Results/ExpectedImages/{}".format(dirName)
                print(destPath)
                shutil.copytree(testPath, destPath, dirs_exist_ok=True)
                print("removing {}".format(testPath))
                if os.path.isdir(testPath):
                    shutil.rmtree(testPath)

        shutil.copytree("./Results/ExpectedImages", "./ExpectedImages/{}".format(target), dirs_exist_ok=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Target Options')
    parser.add_argument('--target', type=str, help='optional target name', default="Default")
    args = parser.parse_args()
    RenameImageFileNames(args.target)
