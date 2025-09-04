import xml.etree.ElementTree
import os
import re
import glob
import sys
import time

def readXML(INPUT_FILE):
    X3D = xml.etree.ElementTree.parse(INPUT_FILE)
    root = X3D.getroot()
    return root
