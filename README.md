# Requirements:
* bash, echo, rm, ex, curl (or ignore errors)
* nodejs (npx)
* castle-model-viewer 5.3.0 (castle-model-converter)
* python 3

# NOTE:

Not all joints or the humanoid are mapped yet.  WIP.

Feedback on joint mapping in cc2v2.py and alienmap.py is welcome, should be self-explanatory.

Suggestions on naming interpolators is also welcome.

No scaling is done, yet.

# Input files -- configure in runwalkingman.py
walking_man_cc_test.new.python.x3d
WalkingAlien.gltf, scene.bin (downloaded)
textures/* (downloaded)

# Output files -- configure in runwalkingman.py runwalkingalienX_ITE.py and batcheverything.sh

walking_man_cc_test_joints_mapped.x3d  -- intermediate file
walking_man_cc_test_interpolators_mapped.x3d -- final file
WalkingAlienFinalOutputX_ITE.x3dv -- WalkingAlien.gltf conversion

# Filenames, Prefixes and TimeSensors are configured by editing runwalkingman.py

* INPUT_PREFIX  -- HAnim prefix found in input file (current ignored)
* INPUT_FILE    -- Input file
* OUTPUT_PREFIX -- HAnim prefix set during mapping (hanim_ preffered for animations)
* OUTPUT_FILE   -- Intermediate file
* FINAL_FILE    -- Final result file
* TIME_SENSORS  -- array of TimeSensors to rename OrientationInterpolators and PositionInterpolators

# running

bash batcheverything.sh

Then pickup your output files.
