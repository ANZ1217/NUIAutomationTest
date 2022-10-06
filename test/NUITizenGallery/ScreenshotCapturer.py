# test python script must be in same location as aurum_pb2.py

import glob
import os
import re
import shutil
import subprocess
import datetime
import argparse
from distutils.dir_util import copy_tree

# Testcases list.
def GetTCList():
    with open('./tclist.txt') as file:
        lines = file.readlines()
        newlines = list()
        for line in lines:
            line = line.rstrip()
            if not line.startswith('#'):
                newlines.append(line)
        return newlines


def RemoveAllDirs(tcFileNameList, target):
    for item in tcFileNameList:
        print("================{}================".format(item))
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

    args = ["python{}".format(python_version), "-u", "{}{}".format(path_to_run, py_name)]
    with subprocess.Popen(args, universal_newlines=True, stdout=subprocess.PIPE, bufsize=1, stderr=subprocess.PIPE) as proc:
        for line in proc.stdout:
            if 'False' in line:
                print("\033[91m" + line + "\033[0m")
            elif 'True' in line:
                print("\033[92m" + line + "\033[0m")
            else:
                print(line)
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
        print("================ {} Start ============== {}:{}:{}".format(item, now.hour, now.minute, now.second))

        ret = RunTest(item)
        if ret:
            #r = re.compile("([a-zA-Z]+)Test([0-9]+)")
            m = re.match("([a-zA-Z]+)Test([0-9]+)", item)
            dirName = m.group(1)
            #print(dirName)
            imageList = glob.glob("./Results/TestedImages/*")
            print(imageList)
            for testPath in imageList:
                print("{} copying".format(testPath))
                destPath = "./Results/ExpectedImages/{}".format(dirName)
                print(destPath)
                copy_tree(testPath, destPath)
                print("removing {}".format(testPath))
                if os.path.isdir(testPath):
                    shutil.rmtree(testPath)

        copy_tree("./Results/ExpectedImages", "./ExpectedImages/{}".format(target))

        print("================ {} Finish ============== {}:{}:{}".format(item, now.hour, now.minute, now.second))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Target Options')
    parser.add_argument('--target', type=str, help='optional target name', default="Default")
    args = parser.parse_args()
    RenameImageFileNames(args.target)
