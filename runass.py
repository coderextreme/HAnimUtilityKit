from assmap import skeleton_map_list
from HAnimUtility import HAnimUtility

INPUT_PREFIX = "hanim_"
INPUT_FILE = "AnimatedAssembledHumanSkeleton.x3d"
OUTPUT_PREFIX = "hanim_"
FINAL_FILE = "AnimatedAssembledHumanSkeleton_Final.x3d"
TIME_SENSORS = [ "Ex_Time" ]

joe = HAnimUtility()
joe.joe_rename(INPUT_FILE, skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX, TIME_SENSORS, FINAL_FILE)
