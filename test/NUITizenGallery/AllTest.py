# test python script must be in same location as aurum_pb2.py

import re
import subprocess


# Testcases list.
def GetTCList():
    with open('./tclist.txt') as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        return lines


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

    failedCount = 0
    if not error_:
        #print(output)
        items = re.findall("Testing result : .*$", output, re.MULTILINE)
        for x in items:
            print(x)
            if 'Testing result : True' not in x:
                failedCount+=1
    else:
        print(error_)
        failedCount+=1

    return failedCount


def RunAllTest():
    passedCount = 0
    failedCount = 0
    tcFileNameList = GetTCList()
    for item in tcFileNameList:
        print("================{}=======================".format(item))
        fcount = RunTest(item)
        if fcount == 0:
            passedCount+=1
        else:
            failedCount+=1

    # Print results.
    print("total tcs: {}, passed: {}, failed: {}".format(len(tcFileNameList), passedCount, failedCount))


if __name__ == '__main__':                                         
    RunAllTest()
