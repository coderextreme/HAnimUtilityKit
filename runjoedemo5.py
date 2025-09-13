from joemap import skeleton_map_list
from HAnimUtility import HAnimUtility

INPUT_PREFIX = "Joe_"
INPUT_FILE = "JoeDemo5JoeSkin5.x3d"
OUTPUT_PREFIX = "hanim_"
FINAL_FILE = "JoeDemo5JoeSkin5_Final.x3d"
TIME_SENSORS = [ "Ex_Time" ]

joedemo5 = HAnimUtility()
joedemo5.joe_rename(INPUT_FILE, skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX, TIME_SENSORS, FINAL_FILE)
