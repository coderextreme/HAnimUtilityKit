from alienmap import skeleton_map_list
from HAnimUtility import HAnimUtility

INPUT_PREFIX = ""

# This file has animations removed, so no need to remove animations, or rename interpolators
INPUT_FILE = "WalkingAlienTruncated.x3d"
OUTPUT_PREFIX = "hanim_"
FINAL_FILE = "WalkingAlienTruncated_Final.x3d"
TIME_SENSORS = [ ]

alien_truncated = HAnimUtility()
alien_truncated.truncated_rename(INPUT_FILE, skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX, TIME_SENSORS, FINAL_FILE)
