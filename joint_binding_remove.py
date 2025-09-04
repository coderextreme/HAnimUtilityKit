import xml.etree.ElementTree
import os
import re
import glob
import sys
import time

def joint_binding_remove(root):

    humanoids = root.findall(".//HAnimHumanoid")
    for humanoid in humanoids:
        humanoid.attrib.pop("jointBindingPositions")
        humanoid.attrib.pop("jointBindingRotations")
        humanoid.attrib.pop("jointBindingScales")
        #del humanoid.attrib["jointBindingPositions"]
        #del humanoid.attrib["jointBindingRotations"]
        #del humanoid.attrib["jointBindingScales"]
