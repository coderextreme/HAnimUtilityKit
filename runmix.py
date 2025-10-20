from mixmap import skeleton_map_list
from HAnimUtility import HAnimUtility

INPUT_PREFIX = "mixamorig:"
INPUT_FILE = "BodySkinIndexedFaceSetNIST.scaled.x3d"
OUTPUT_PREFIX = "hanim_"
FINAL_FILE = "BodySkinIndexedFaceSetNIST_Final.x3d"
TIME_SENSORS = [ ]

mix = HAnimUtility()
mix.mix_rename(INPUT_FILE, skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX, TIME_SENSORS, FINAL_FILE)
