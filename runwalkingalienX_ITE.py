from alienmap import skeleton_map_list
from HAnimUtility import HAnimUtility

INPUT_PREFIX = ""
INPUT_FILE = "WalkingAlienX_ITE.x3d"
OUTPUT_PREFIX = "hanim_"
FINAL_FILE = "WalkingAlienX_ITE_Final.x3d"
TIME_SENSORS = [ "Timer1" ]

alien_x_ite = HAnimUtility()
alien_x_ite.truncated_rename(INPUT_FILE, skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX, TIME_SENSORS, FINAL_FILE)
