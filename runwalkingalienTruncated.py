from alienmap import skeleton_map_list
from jointmapper import map_joints
from translation_to_center import translation_to_center
from joint_binding_remove import joint_binding_remove

INPUT_PREFIX = ""
INPUT_FILE = "WalkingAlienTruncated.x3d"
OUTPUT_PREFIX = "hanim_"
OUTPUT_FILE = "WalkingAlien_joints_mappedTruncated.x3d"
INTERMEDIATE_FILE = "WalkingAlien_joint_binding_removedTruncated.x3d"
FINAL_FILE = "WalkingAlienFinalOutputTruncated.x3d"
map_joints(INPUT_PREFIX, INPUT_FILE, skeleton_map_list, OUTPUT_PREFIX, OUTPUT_FILE)
joint_binding_remove(OUTPUT_FILE, INTERMEDIATE_FILE)
translation_to_center(INTERMEDIATE_FILE, FINAL_FILE)

