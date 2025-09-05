from cc2v2 import skeleton_map_list
from HAnimUtility import HAnimUtility

INPUT_PREFIX = "CC_"
INPUT_FILE = "walking_man_cc_test.new.python.x3d"
OUTPUT_PREFIX = "hanim_"
FINAL_FILE = "walking_man_cc_test_Final.x3d"
TIME_SENSORS = [ "JohnWalkTimer" ]

man = HAnimUtility()
man.standard_rename(INPUT_FILE, skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX, TIME_SENSORS, FINAL_FILE)
