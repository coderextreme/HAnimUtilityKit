from joemap import skeleton_map_list
from HAnimUtility import HAnimUtility

INPUT_PREFIX = "Joe_"
INPUT_FILE = "JoeHAnimKick1a.x3d"
OUTPUT_PREFIX = "hanim_"
FINAL_FILE = "JoeHAnimKick1a_Final.x3d"
TIME_SENSORS = [ "Ex_Time" ]

joe = HAnimUtility()
joe.standard_rename(INPUT_FILE, skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX, TIME_SENSORS, FINAL_FILE)
