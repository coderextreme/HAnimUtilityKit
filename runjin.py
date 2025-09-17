from joemap import skeleton_map_list
from HAnimUtility import HAnimUtility

INPUT_PREFIX = "Joe_"
INPUT_FILE = "JinLOA4.scaled1.x3d"
OUTPUT_PREFIX = "hanim_"
FINAL_FILE = "JinLOA4.scaled1_Final.x3d"
TIME_SENSORS = [ "Ex_Time" ]

jin = HAnimUtility()
jin.jin_remove_animations(INPUT_FILE, skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX, TIME_SENSORS, FINAL_FILE)
