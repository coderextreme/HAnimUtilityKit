from joemap import skeleton_map_list
from jointmapper import map_joints
from rename_interpolators import rename_interpolators

INPUT_PREFIX = "Joe_"
INPUT_FILE = "JoeHAnimKick1a.x3d"

OUTPUT_PREFIX = "hanim_"
OUTPUT_FILE = "JoeHAnimKick1a_joints_mapped.x3d"
map_joints(INPUT_PREFIX, INPUT_FILE, skeleton_map_list, OUTPUT_PREFIX, OUTPUT_FILE)

FINAL_FILE = "JoeHAnimKick1a_interpolators_mapped.x3d"
TIME_SENSORS = [ "Ex_Time" ]
rename_interpolators(OUTPUT_FILE, TIME_SENSORS, FINAL_FILE)
