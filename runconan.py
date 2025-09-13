from conanmap import skeleton_map_list
from HAnimUtility import HAnimUtility

INPUT_PREFIX = "GameSkeleton_"
INPUT_FILE = "conan_23_Aug2025.scaled.x3d"
OUTPUT_PREFIX = "hanim_"
FINAL_FILE = "conan_23_Aug2025_Final.x3d"
TIME_SENSORS = [ "JohnJumpTimer" ]

conan = HAnimUtility()
conan.standard_rename(INPUT_FILE, skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX, TIME_SENSORS, FINAL_FILE)
