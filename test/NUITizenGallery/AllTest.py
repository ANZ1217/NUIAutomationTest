# test python script must be in same location as aurum_pb2.py

import re
import subprocess


# Testcases list.
def GetTCList():
    with open('./tclist.txt') as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        return lines


def RunTest(pyFileName, ret):
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
            if 'Testing result : True' not in x:
                print("\033[91m" + x + "\033[0m")
                failedCount+=1
            else:
                print("\033[92m" + x + "\033[0m")
            ret.write(x + "\n")
    else:
        print("\033[41m\033[37m"+ error_ + "\033[0m")
        ret.write(error_ + "\n")
        failedCount+=1

    return failedCount


def RunAllTest(ret):
    passedCount = 0
    failedCount = 0
    failedTest = ""
    tcFileNameList = GetTCList()
    for item in tcFileNameList:
        itemTitle = "====================[ {} ]=======================".format(item)
        print("\033[47m\033[30m" + itemTitle + "\033[0m")
        ret.write(itemTitle + "\n")
        fcount = RunTest(item, ret)
        if fcount == 0:
            passedCount+=1
        else:
            failedCount+=1
            failedTest+=item+" "

    # Print results.
    tcCount = "Total TCs: {}".format(len(tcFileNameList))
    pCount = "Passed: {}, ".format(passedCount)
    fCount = "Failed: {}".format(failedCount)
    resultTitle = "====================[ {} ]=======================".format(tcCount)
    print("\033[48;5;33m\033[38;5;235m" + resultTitle + "\033[0m")
    ret.write(resultTitle+ "\n")
    print("\033[92m" + pCount + "\033[91m" + fCount + "\033[0m")
    ret.write(pCount + fCount + "\n")
    if failedCount != 0:
        failedList = "Falied Test : [{}]".format(failedTest)
        print("\033[38;5;214m" + failedList + "\033[0m")
        ret.write(failedList + "\n")
    print("Result log is written in ./result.txt")

if __name__ == '__main__':
    f = open("./result.txt", "w")
    RunAllTest(f)
    f.close()
