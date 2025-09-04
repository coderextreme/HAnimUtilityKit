import xml.etree.ElementTree
import os
import re
import glob
import sys
import time

def swap_translation_center(parent_joint, parent_translation):

    child_joints = parent_joint.findall('HAnimJoint')
    for child_joint in child_joints:
        child_translation = child_joint.get("translation", "0 0 0")
        print(f"child {child_joint.get('DEF')} {child_translation}")
        translationp = [float(val) for val in parent_translation.split()]
        translationc = [float(val) for val in child_translation.split()]

        sum_translation = [a + b for a, b in zip(translationp, translationc)]

        summed_translation = ' '.join(map(str, sum_translation))
        child_joint.set("center", summed_translation)
        child_joint.set("translation", "0 0 0")
        child_joint.set("rotation", "0 1 0 0")
        swap_translation_center(child_joint, summed_translation)

def translation_to_center(root):

    parent_joints = root.findall(".//HAnimHumanoid/HAnimJoint")
    for parent_joint in parent_joints:
        if parent_joint.get('DEF'):
            joint_translation = parent_joint.get("translation", "0 0 0")
            print(f"joint {parent_joint.get('DEF')} {joint_translation}")
            parent_joint.set("center", joint_translation)
            parent_joint.set("translation", "0 0 0")
            parent_joint.set("rotation", "0 1 0 0")
            swap_translation_center(parent_joint, joint_translation)
