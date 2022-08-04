# test python script must be in same location as aurum_pb2.py

import glob
import os
import re
import shutil
import subprocess
import datetime

# Testcases list.
def GetTCList():
    with open('./tclist.txt') as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        return lines


def RemoveAllDirs(tcFileNameList):
    for item in tcFileNameList:
        print("================{}=======================".format(item))
        r = re.compile("([a-zA-Z]+)Test([0-9]*)")
        m = r.match(item)
        dirName = m.group(1)
        print('Directory {} is removed.'.format(dirName))
        path = './'+dirName
        if os.path.isdir(path):
            shutil.rmtree(path)  # remove dir and all contains


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


def RenameImageFileNames():
    passedCount = 0
    failedCount = 0
    tcFileNameList = GetTCList()

    # Remove all directories.
    RemoveAllDirs(tcFileNameList)

    # Generate screenshots expected.
    for item in tcFileNameList:
        now = datetime.datetime.now()
        print("================{}============== {}:{}:{}".format(item, now.hour, now.minute, now.second))

        ret = RunTest(item)
        if ret:
            r = re.compile("([a-zA-Z]+)Test([0-9]+)")
            m = r.match(item)
            dirName = m.group(1)
            #print(dirName)
            imageList = glob.glob("./{}/*.png".format(dirName))
            for fileName in imageList:
                print("File {} would be renamed.".format(fileName))
                if 'Expected' not in fileName:
                    r0 = re.compile("./([a-zA-Z]+)/([a-zA-Z]+)([0-9]+).png")
                    m0 = r0.match(fileName)
                    os.rename(fileName, './{}/{}Expected{}.png'.format(dirName, m0.group(2), m0.group(3)))


if __name__ == '__main__':                                         
    RenameImageFileNames()
