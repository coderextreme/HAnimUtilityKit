from alienmap import skeleton_map_list
from rootmapper import map_joints
from translation_to_center import translation_to_center
from joint_binding_remove import joint_binding_remove
from tangent_remove import tangent_remove
from readXML import readXML
from writeXML import writeXML

INPUT_PREFIX = ""
INPUT_FILE = "WalkingAlienTruncated.x3d"
OUTPUT_PREFIX = "hanim_"
FINAL_FILE = "WalkingAlienTruncated_Final.x3d"
root = readXML(INPUT_FILE)
map_joints(root, skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX)
joint_binding_remove(root)
tangent_remove(root)
translation_to_center(root)
writeXML(root, FINAL_FILE)
