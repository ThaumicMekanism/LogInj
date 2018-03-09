#!/usr/bin/env python

'''
    Created by Stephan Kaminsky to inject separate subcircuit files into one circuit file in logisim.
'''

version = "1.0.4"
updateurl = "https://raw.githubusercontent.com/ThaumicMekanism/LogisimInjector/master/inject.py"

import sys
import re
import xml.etree.ElementTree
import os
import datetime
from shutil import copyfile
from shutil import move
import urllib.request
from distutils.version import StrictVersion

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        choice = input(question + prompt)
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

print("\n#####################################################################################")
print("Logisim Injector by Stephan Kaminsky v" + version + "\nCheck for updates here: https://github.com/ThaumicMekanism/LogisimInjector")
print("#####################################################################################\n")
etext = "[INFO] Checking for updates..."
print(etext, end="\r")
try:
    urldata = urllib.request.urlopen(updateurl).read().decode("utf-8", "ignore")
    if version in urldata:
        print(etext + "Done!\n[INFO] This is the latest version!")
    else:
        m = re.search("version = \"(.+?)\"", urldata)
        newestv = m.group(1)
        if StrictVersion(newestv) > StrictVersion(version):
            print(etext + "Done!\n[WARNING] This is not the latest version! Newer version v" + newestv + " detected!")
            if query_yes_no("Do you want to update the script?"):
                directory, name = os.path.split(__file__)
                updateurl = "https://raw.githubusercontent.com/ThaumicMekanism/LogisimInjector/master/inject.py"
                updatename = "update.py"
                urllib.request.urlretrieve(updateurl, updatename)
                move(updatename, name)
                print("Updated! Executing updated script...\n-------------------------------------------------------------------------------------\n")
                exec(compile(open(name, "rb").read(), name, 'exec'))
                exit(0)
        else:
            print(etext + "Done!\n[INFO] You are on a newer version.")
except Exception as e:
    print(etext + "ERROR!\n[ERROR] Could not check if this is the latest version!")

print()
if (len(sys.argv) != 4):
    print("[ERROR] Please make sure you have inputed the four arguments: destination_file source_file source_circ_name");
    exit(-1);


dest_file = str(sys.argv[1])
source_file = str(sys.argv[2])
source_circ_name = str(sys.argv[3])



#Backing up destination file just in case...
FilePath = dest_file
modifiedTime = os.path.getmtime(FilePath)
timeStamp =  datetime.datetime.fromtimestamp(modifiedTime).strftime("%b-%d-%y-%H.%M.%S")
newname = os.path.realpath(FilePath) + "_preinj_" + timeStamp + ".bak"
copyfile(os.path.realpath(FilePath), newname)


print("[INFO] Attempting to add subcircuit '" + source_circ_name + "' in file '" + source_file + "' to the destination file '" + dest_file + "'...\n")

etext = "[INFO] Parsing destination file's xml..."
print(etext, end="\r")
try:
    dest_xml = xml.etree.ElementTree.parse(dest_file)
except Exception as e:
    print("\n[ERROR] An error has occured!\n")
    raise e
print(etext + "Done!\n")

etext = "[INFO] Parsing source file's xml..."
print(etext, end="\r")
try:
    source_xml = xml.etree.ElementTree.parse(source_file)
except Exception as e:
    print("\n[ERROR] An error has occured!\n")
    raise e
print(etext + "Done!\n")

source_circ_xml = None
for subcirc in source_xml.findall('circuit'):
    if (subcirc.get('name') == source_circ_name):
        source_circ_xml = subcirc
        break

if (source_circ_xml == None):
    print("[ERROR] Could not find subcircuit '" + source_circ_name + "' in source file '" + source_file + "'!")
    exit(-1);

print("[INFO] Found subcircuit '" + source_circ_name + "' in source file '" + source_file + "'!\n")

for subcirc in dest_xml.findall('circuit'):
    if (subcirc.get('name') == source_circ_name):
        if query_yes_no("A circuit with the name '" + source_circ_name + "' was already found in the source file! Do you want to remove it to add the new circuit?"):
            print("[INFO] Removing...", end="\r")
            dest_xml.getroot().remove(subcirc)
            print("[INFO] Removing...Done!")
        else:
            if not query_yes_no("Do you still want to continue to add the duplicate circuit?"):
                print("[WARNING] Exiting...")
                exit(0)

etext = "[INFO] Editing destination file..."
print(etext, end="\r")
dest_xml.getroot().append(source_circ_xml)
dest_xml.write(dest_file)
print(etext + "Done!")
print("[Success]")
exit(0)