from joemap import skeleton_map_list
from rootmapper import map_joints
from root_rename_interpolators import rename_interpolators
from animation_remove import animation_remove
from readXML import readXML
from writeXML import writeXML

INPUT_PREFIX = "Joe_"
INPUT_FILE = "JoeDemo5JoeSkin5.x3d"
OUTPUT_PREFIX = "hanim_"
FINAL_FILE = "JoeDemo5JoeSkin5_Final.x3d"
TIME_SENSORS = [ "Ex_Time" ]

root = readXML(INPUT_FILE)
animation_remove(root)
map_joints(root, skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX)
# rename_interpolators(root, TIME_SENSORS)
writeXML(root, FINAL_FILE)
