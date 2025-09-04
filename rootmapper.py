import xml.etree.ElementTree
import os
import re
import glob
import sys
import time

def map_joints(root, skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX):

    # Sort by input name length, descending
    # This is CRITICAL to prevent partial replacements (e.g., "l_hip" replacing part of "l_hip_rotation" if not handled)
    # Though in this specific HAnim case, CC names are usually distinct enough that alphabetical is okay,
    # but length-based is safer for general text replacement.

    sorted_skeleton_map = sorted(skeleton_map_list, key=lambda x: len(x[0]), reverse=True)

    for cc_name, v2_name in sorted_skeleton_map:

        # prepend something to the Joint for DEF

        prepended_joint = OUTPUT_PREFIX+v2_name

        def_joints = root.findall(".//HAnimJoint[@DEF='"+cc_name+"']")
        for def_joint in def_joints:
            def_joint_name = def_joint.get("DEF")
            if def_joint_name == cc_name:
                def_joint.set("DEF", prepended_joint)
                def_joint.set("name", v2_name)
            # ROUTEs don't have USE
            rotation_joint_routes = root.findall(".//ROUTE[@toNode='"+def_joint_name+"'][@toField='set_rotation']")
            for rotation_joint_route in rotation_joint_routes:
                rotation_joint_route.set("toNode", prepended_joint)
            translation_joint_routes = root.findall(".//ROUTE[@toNode='"+def_joint_name+"'][@toField='set_translation']")
            for translation_joint_route in translation_joint_routes:
                translation_joint_route.set("toNode", prepended_joint)

        use_joints = root.findall(".//HAnimJoint[@USE='"+cc_name+"']")
        for use_joint in use_joints:
            use_joint_name = use_joint.get("USE")
            if use_joint_name == cc_name:
                use_joint.set("USE", prepended_joint)
