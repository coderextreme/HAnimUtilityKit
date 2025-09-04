from alienmap import skeleton_map_list
from rootmapper import map_joints
from root_rename_interpolators import rename_interpolators
from animation_remove import animation_remove
from translation_to_center import translation_to_center
from joint_binding_remove import joint_binding_remove
from tangent_remove import tangent_remove
from readXML import readXML
from writeXML import writeXML

INPUT_PREFIX = ""
INPUT_FILE = "WalkingAlienX_ITE.x3d"
OUTPUT_PREFIX = "hanim_"
FINAL_FILE = "WalkingAlienX_ITE_Final.x3d"
TIME_SENSORS = [ "Timer1" ]

root = readXML(INPUT_FILE)
animation_remove(root)
map_joints(root, skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX)
# rename_interpolators(root, TIME_SENSORS)
joint_binding_remove(root)
tangent_remove(root)
translation_to_center(root)
writeXML(root, FINAL_FILE)
