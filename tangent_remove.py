import xml.etree.ElementTree
import os
import re
import glob
import sys
import time

def tangent_remove(root):

    for tangent_parent in root.findall('.//Tangent/..'):
        for tangent in tangent_parent.findall('Tangent'):
            tangent_parent.remove(tangent)
