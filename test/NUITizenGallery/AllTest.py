# test python script must be in same location as aurum_pb2.py

import os
import re
import shutil
import subprocess
import time
import argparse
from distutils.dir_util import copy_tree

# Testcases list.
def GetTCList(filelist):
    with open(filelist) as file:
        lines = file.readlines()
        newlines = list()
        for line in lines:
            line = line.rstrip()
            if not line.startswith('#'):
                newlines.append(line)
        return newlines


def RunTest(pyFileName, ret):
    python_version = '3'
    path_to_run = './'
    py_name = pyFileName + '.py'
    failedCount = 0

    args = ["python{}".format(python_version), "-u", "{}{}".format(path_to_run, py_name), "--no-exit"]
    proc = subprocess.Popen(args, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with subprocess.Popen(args, universal_newlines=True, stdout=subprocess.PIPE, bufsize=1, stderr=subprocess.PIPE) as proc:
        for line in proc.stdout:
            if 'False' in line:
                failedCount+=1
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
        failedCount+=1
        print("\033[41m\033[37m"+ error_ + "\033[0m")

    return failedCount


def RunAllTest(list, ret, currentTime, target):
    passedCount = 0
    failedCount = 0
    failedTest = ""

    testDate = time.strftime('%Y-%m-%d %H:%M')
    ret.write("<head><title>NUITizenGallery All Test {}</title></head>\n".format(testDate))
    ret.write("<body>\n<h1>NUITizenGallery All Test {}</h1>\n".format(testDate))
    ret.write("<table border=1>\n<th>Test</th>\n<th>Result</th>\n");

    tcFileNameList = GetTCList(list)
    for item in tcFileNameList:
        itemTitle = "=============================[ {} ]=============================".format(item)
        print("\033[47m\033[30m" + itemTitle + "\033[0m")

        fcount = RunTest(item, ret)
        if fcount == 0:
            passedCount+=1
            ret.write("<tr>\n<td width=500>" + item + "</td>\n<td width=150 style=\"text-aglign: center\"><span style=\"color: #006600\">Pass</span></td>\n</tr>\n")
        else:
            failedCount+=1
            failedTest+=item+" "
            ret.write("<tr>\n<td width=500>" + item + "</td>\n<td width=150 style=\"text-aglign: center\"><span style=\"color: #CC0000\">Failed</span></td>\n</tr>\n")

    ret.write("</table>\n")

    # Print results.
    tcCount = "Total TCs: {}".format(len(tcFileNameList))
    pCount = "Passed: {}".format(passedCount)
    fCount = "Failed: {}".format(failedCount)
    resultTitle = "=============================[ {} ]=============================".format(tcCount)
    print("\033[48;5;33m\033[38;5;235m" + resultTitle + "\033[0m")
    ret.write("<p><b>" + resultTitle+ "<br>\n")
    print("\033[92m" + pCount + ", \033[91m" + fCount + "\033[0m")
    ret.write("<span style=\"color: #006600\">" + pCount + "</span>, <span style=\"color: #CC0000\">" + fCount + "<span><br>\n")
    if failedCount != 0:
        failedCase = "Failed Test : [{}]".format(failedTest)
        print("\033[38;5;214m" + failedCase + "\033[0m")
        ret.write("<i>" + failedCase + "</i><br>\n")
        f1 = open("./Results/failedlist.txt", "w")
        failedList = failedTest.split()
        for tc in failedList:
            f1.write(tc+"\n");
        f1.close()


    ret.write("</b></p>\n</body>\n")
    print("Result log is written in ./Results/{}/result.hmtl".format(currentTime))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Target Options')
    parser.add_argument('--target', type=str, help='optional target name')
    args = parser.parse_args()
    currentTime = time.strftime('%Y-%m-%d_%H:%M')
    os.makedirs("./Results/"+currentTime, exist_ok=True)
    f = open("./Results/{}/result.html".format(currentTime), "w")
    f.write("<html>\n")
    RunAllTest('./tclist.txt', f, currentTime, args.target)
    f.write("</html>")
    f.close()
    copy_tree("./Results/TestedImages", "./Results/{}/TestedImages".format(currentTime))
    copy_tree("./Results/ExpectedImages", "./Results/{}/ExpectedImages".format(currentTime))
    if os.path.islink("./Results/Latest"):
        os.remove("./Results/Latest")
        os.symlink("./Results/{}".format(currentTime), "./Results/Latest")
