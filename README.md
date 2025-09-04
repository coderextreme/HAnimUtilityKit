# Requirements:
* bash, echo, rm, ex, curl (or ignore errors)
* nodejs (npx)
* castle-model-viewer 5.3.0 (castle-model-converter)
* python 3

# NOTE:

Not all joints or the humanoid are mapped yet.  WIP.

Feedback on joint mappings in
```
cc2v2.py
alienmap.py
conanmap.py
joemap.py
jointmapper.py
```
is welcome, should be self-explanatory.

Suggestions on naming interpolators is also welcome.

No scaling is done, yet.

# Output files -- configure in runwalkingman.py runwalkingalienX_ITE.py and batcheverything.sh

JoeDemo5JoeSkin5_Final.x3dv
JoeHAnimKick1a_Final.x3dv
WalkingAlienTruncated_Final.x3dv
conan_23_Aug2025_Final.x3dv
walking_man_cc_test_Final.x3dv

# Filenames, Prefixes and TimeSensors are configured by editing runwalkingman.py

* INPUT_PREFIX  -- HAnim prefix found in input file (current ignored)
* INPUT_FILE    -- Input file
* OUTPUT_PREFIX -- HAnim prefix set during mapping (hanim_ preffered for animations)
* OUTPUT_FILE   -- Intermediate file
* FINAL_FILE    -- Final result file
* TIME_SENSORS  -- array of TimeSensors to rename OrientationInterpolators and PositionInterpolators

# running

bash batcheverything.sh
bash batchtruncated.sh

Then pickup your output files.
