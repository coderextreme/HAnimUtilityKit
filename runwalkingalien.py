from alienmap import skeleton_map_list
from HAnimUtility import HAnimUtility

INPUT_PREFIX = ""
INPUT_FILE = "WalkingAlien.x3d"
OUTPUT_PREFIX = "hanim_"
FINAL_FILE = "WalkingAlien_Final.x3d"
TIME_SENSORS = [ "Timer1" ]

alien = HAnimUtility()
alien.tidy_rename(INPUT_FILE, skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX, TIME_SENSORS, FINAL_FILE)
