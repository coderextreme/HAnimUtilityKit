from alienmap import skeleton_map_list
from jointmapper import map_joints
from translation_to_center import translation_to_center

INPUT_PREFIX = ""
INPUT_FILE = "WalkingAlienTruncated.x3d"
OUTPUT_PREFIX = "hanim_"
OUTPUT_FILE = "WalkingAlien_joints_mappedTruncated.x3d"
FINAL_FILE = "WalkingAlienFinalOutputTruncated.x3d"
map_joints(INPUT_PREFIX, INPUT_FILE, skeleton_map_list, OUTPUT_PREFIX, OUTPUT_FILE)
translation_to_center(INPUT_FILE, FINAL_FILE)

