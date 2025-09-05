# Requirements:
* bash, echo, rm, ex, curl (or ignore errors)
* nodejs (npx)
* castle-model-viewer 5.3.0 (castle-model-converter)
* python 3

# NOTE:

Not all joints or the humanoid are mapped yet.  WIP.

Feedback on joint mappings in
```
alienmap.py
conanmap.py
joemap.py
manmap.py
```
is welcome, should be self-explanatory.

Suggestions on naming interpolators is also welcome.

No scaling is done, yet.

# Output files

### Preferred
```
JoeDemo5JoeSkin5_Final.x3dv
JoeHAnimKick1a_Final.x3dv
WalkingAlien_Final.x3dv
conan_23_Aug2025_Final.x3dv
walking_man_cc_test_Final.x3dv
```

### Deprecated
```
JoeDemo5JoeSkin5_x3dom.x3d
JoeHAnimKick1a_x3dom.x3d
WalkingAlien_x3dom.x3d
conan_23_Aug2025_x3dom.x3d
walking_man_cc_test_x3dom.x3d
```

### Filenames, Prefixes and TimeSensors

* INPUT_PREFIX  -- HAnim prefix found in input file (current ignored)
* INPUT_FILE    -- Input file
* OUTPUT_PREFIX -- HAnim prefix set during mapping (hanim_ preffered for animations)
* FINAL_FILE    -- Final result file
* TIME_SENSORS  -- array of TimeSensors to rename OrientationInterpolators and PositionInterpolators

## The above are configured in:
```
runconan.py
runjoe.py
runjoedemo5.py
runwalkingalien.py
runwalkingman.py
```

# Running

```bash
bash batcheverything.sh
```

Then pickup your output files.
