# test python script must be in same location as aurum_pb2.py

import os
import re
import shutil
import subprocess
import time
import argparse

# Testcases list.
def GetTCList(list):
    with open(list) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        return lines


def RunTest(pyFileName, ret):
    python_version = '3'
    path_to_run = './'
    py_name = pyFileName + '.py'

    args = ["python{}".format(python_version), "{}{}".format(path_to_run, py_name), "--no-exit"]
    #print(args)
    proc = subprocess.Popen(args, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        output, error_ = proc.communicate(timeout=120)
    except subprocess.TimeoutExpired:
        proc.kill()
        output, error_ = proc.communicate()

    failedCount = 0
    if not error_:
        #print(output)
        outputlines = output.split('\n')
        for printline in outputlines:
            if 'True' in printline:
                print("\033[92m" + printline + "\033[0m")
            elif 'False' in printline:
                print("\033[91m" + printline + "\033[0m")
                failedCount+=1
            else:
                print(printline)
    else:
        print("\033[41m\033[37m"+ error_ + "\033[0m")
        failedCount+=1

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
        if item.startswith('#'):
            #print("{} will not be tested.".format(item))
            continue

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
    shutil.copytree("./Results/TestedImages", "./Results/{}/TestedImages".format(currentTime), dirs_exist_ok=True)
    shutil.copytree("./Results/ExpectedImages", "./Results/{}/ExpectedImages".format(currentTime), dirs_exist_ok=True)
    if os.path.islink("./Results/Latest"):
        os.remove("./Results/Latest")
        os.symlink("./Results/{}".format(currentTime), "./Results/Latest")
