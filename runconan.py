from conanmap import skeleton_map_list
from jointmapper import map_joints
from rename_interpolators import rename_interpolators

INPUT_PREFIX = "GameSkeleton_"
INPUT_FILE = "conan_23_Aug2025.x3d"

OUTPUT_PREFIX = "hanim_"
OUTPUT_FILE = "conan_23_Aug2025_joints_mapped.x3d"
map_joints(INPUT_PREFIX, INPUT_FILE, skeleton_map_list, OUTPUT_PREFIX, OUTPUT_FILE)

FINAL_FILE = "conan_23_Aug2025_interpolators_mapped.x3d"
TIME_SENSORS = [ "JumpTimer" ]
rename_interpolators(OUTPUT_FILE, TIME_SENSORS, FINAL_FILE)
