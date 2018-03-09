#!/usr/bin/env python

'''
    Created by Stephan Kaminsky to inject separate subcircuit files into one circuit file in logisim.
'''

import sys
import xml.etree.ElementTree
import os
import datetime
from shutil import copyfile

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


print("[INFO] Attempting to add subcircuit '" + source_circ_name + "' in file '" + source_file + "' to the destination file '" + dest_file + "'\n")

try:
    print("[INFO] Parsing destination file's xml...")
    dest_xml = xml.etree.ElementTree.parse(dest_file)
except Exception as e:
    print("\n[ERROR] An error has occured!\n")
    raise e
print("[INFO] Parsing succeeded!\n")

try:
    print("[INFO] Parsing source file's xml...")
    source_xml = xml.etree.ElementTree.parse(source_file)
except Exception as e:
    print("\n[ERROR] An error has occured!\n")
    raise e
print("[INFO] Parsing succeeded!\n")

source_circ_xml = None
for subcirc in source_xml.findall('circuit'):
    if (subcirc.get('name') == source_circ_name):
        source_circ_xml = subcirc
        break

if (source_circ_xml == None):
    print("[ERROR] Could not find subcircuit '" + source_circ_name + "' in source file '" + source_file + "'!")
    exit(-1);

print("[INFO] Found subcircuit '" + source_circ_name + "' in source file '" + source_file + "'!\n")


dest_xml.getroot().append(source_circ_xml)
dest_xml.write(dest_file)
print("[Success]")
exit(0)