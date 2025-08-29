from cc2v2 import skeleton_map_list
from jointmapper import map_joints
from rename_interpolators import rename_interpolators

INPUT_PREFIX = "CC_"
INPUT_FILE = "walking_man_cc_test.new.python.x3d"
OUTPUT_PREFIX = "John_"
OUTPUT_FILE = "walking_man_cc_test_joints_mapped.x3d"
map_joints(INPUT_PREFIX, INPUT_FILE, skeleton_map_list, OUTPUT_PREFIX, OUTPUT_FILE)

FINAL_FILE = "walking_man_cc_test_interpolators_mapped.x3d"
TIME_SENSORS = [ "WalkTimer" ]
rename_interpolators(OUTPUT_FILE, TIME_SENSORS, FINAL_FILE)
