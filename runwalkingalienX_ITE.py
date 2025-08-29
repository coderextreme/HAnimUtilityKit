from alienmap import skeleton_map_list
from jointmapper import map_joints
from rename_interpolators import rename_interpolators

INPUT_PREFIX = ""
INPUT_FILE = "WalkingAlienX_ITE.x3d"
OUTPUT_PREFIX = "hanim_"
OUTPUT_FILE = "WalkingAlienJointsMappedX_ITE.x3d"
map_joints(INPUT_PREFIX, INPUT_FILE, skeleton_map_list, OUTPUT_PREFIX, OUTPUT_FILE)

FINAL_FILE = "WalkingAlienFinalOutputX_ITE.x3d"
TIME_SENSORS = [ "Timer1" ]
rename_interpolators(OUTPUT_FILE, TIME_SENSORS, FINAL_FILE)
