import xml.etree.ElementTree
import os
import re
import glob
import sys
import time

def joint_binding_remove(INPUT_FILE, OUTPUT_FILE):

    X3D = xml.etree.ElementTree.parse(INPUT_FILE)
    root = X3D.getroot()

    humanoids = root.findall(".//HAnimHumanoid")
    for humanoid in humanoids:
        humanoid.attrib.pop("jointBindingPositions")
        humanoid.attrib.pop("jointBindingRotations")
        humanoid.attrib.pop("jointBindingScales")
        #del humanoid.attrib["jointBindingPositions"]
        #del humanoid.attrib["jointBindingRotations"]
        #del humanoid.attrib["jointBindingScales"]

    header = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE X3D PUBLIC "ISO//Web3D//DTD X3D 4.0//EN" "https://www.web3d.org/specifications/x3d-4.0.dtd">'
    xmlstr = xml.etree.ElementTree.tostring(root, encoding='unicode')

    xmlString = f"{header}{xmlstr}"
    file_output = os.path.join("./",os.path.basename(OUTPUT_FILE))
    with open(file_output, "w") as output_file:
        output_file.write(xmlString)
