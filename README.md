# NOTE:

Not all joints or the humanoid are mapped yet.  WIP.

Feedback on joint mapping in cc2v2.py is welcome, should be self-explanatory

Suggestions on naming interpolators is also welcom

No scaling is done

# run these two commands, in order
python cc2v2.py
python expression.py

# Input file (must use this, hard-coded)
walking_man_cc_test.new.python.x3d

# Output file (must use this, hard-coded, both should be viewable, overwrites, so make backups)
interpolators_mapped.x3d
joints_mapped.x3d

Filenames, Prefixes and TimeSensors are configured by editing

runwalkingman.py

INPUT_PREFIX  # HAnim prefix found in input file
INPUT_FILE    # Input file
OUTPUT_PREFIX # HAnim prefix set during mapping
OUTPUT_FILE   # Intermediate file
FINAL_FILE    # Final result file
TIME_SENSORS  # array of TimeSensors to rename OrientationInterpolators
