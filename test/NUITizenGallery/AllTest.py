# test python script must be in same location as aurum_pb2.py

import os
import re
import subprocess
import time


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
    else:
        print("\033[41m\033[37m"+ error_ + "\033[0m")
        failedCount+=1

    return failedCount


def RunAllTest(ret):
    passedCount = 0
    failedCount = 0
    failedTest = ""

    testDate = time.strftime('%Y-%m-%d %H:%M')
    f.write("<head><title>NUITizenGallery All Test {}</title></head>\n".format(testDate))
    f.write("<body>\n<h1>NUITizenGallery All Test {}</h1>\n".format(testDate))
    f.write("<table border=1>\n<th>Test</th>\n<th>Result</th>\n");

    tcFileNameList = GetTCList()
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

    f.write("</table>\n")

    # Print results.
    tcCount = "Total TCs: {}".format(len(tcFileNameList))
    pCount = "Passed: {}".format(passedCount)
    fCount = "Failed: {}".format(failedCount)
    resultTitle = "=============================[ {} ]=============================".format(tcCount)
    print("\033[48;5;33m\033[38;5;235m" + resultTitle + "\033[0m")
    ret.write("<p><b>" + resultTitle+ "<br>\n")
    print("\033[92m" + pCount + ", \033[91m" + fCount + "\033[0m")
    ret.write("<span style=\"color: #006600\">" + pCount + "<\span>, <span style=\"color: #CC0000\">" + fCount + "<span><br>\n")
    if failedCount != 0:
        failedList = "Failed Test : [{}]".format(failedTest)
        print("\033[38;5;214m" + failedList + "\033[0m")
        ret.write("<i>" + failedList + "</i><br>\n")

    f.write("</b></p>\n</body>\n")
    print("Result log is written in ./result.hmtl")

if __name__ == '__main__':
    os.makedirs("result", exist_ok=True)
    f = open("./result/result_{}.html".format(time.strftime('%Y-%m-%d_%H:%M')), "w")
    f.write("<html>\n")
    RunAllTest(f)
    f.write("</html>")
    f.close()
