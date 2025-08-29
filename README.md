# NOTE:

Not all joints or the humanoid are mapped yet.  WIP.

Feedback on joint mapping in cc2v2.py is welcome, should be self-explanatory

Suggestions on naming interpolators is also welcome

No scaling is done, yet

# Input file -- configure in runwalkingman.py
walking_man_cc_test.new.python.x3d

# Output files -- configure in runwalkingman.py
joints_mapped.x3d  -- intermediate file
interpolators_mapped.x3d -- final file

# Filenames, Prefixes and TimeSensors are configured by editing runwalkingman.py

* INPUT_PREFIX  -- HAnim prefix found in input file
* INPUT_FILE    -- Input file
* OUTPUT_PREFIX -- HAnim prefix set during mapping
* OUTPUT_FILE   -- Intermediate file
* FINAL_FILE    -- Final result file
* TIME_SENSORS  -- array of TimeSensors to rename OrientationInterpolators


# running

python runwalkingman.py

Then pickup your files in the wherever you put them
