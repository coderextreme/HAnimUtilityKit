echo "Mapping joints and interpolators..."
python runwalkingalienTruncated.py

echo "Converting Final Output from .x3d to .x3dv..."
npx x3d-tidy@latest -i WalkingAlienFinalOutputTruncated.x3d -o WalkingAlienFinalOutputTruncated.x3dv

echo "Touchups before finding validating..."
(echo '%s/PROFILE Interchange/PROFILE Immersive/'; echo g/colorSpaceConversion/d;  echo wq;) > ex7.cmds
ex WalkingAlienFinalOutputTruncated.x3dv < ex7.cmds

echo "Adding animations..."
cat Animations2.x3dv >> WalkingAlienFinalOutputTruncated.x3dv

echo "Validating..."
~/Downloads/castle-model-viewer-5.3.0-win64-x86_64/castle-model-viewer/castle-model-converter.exe --validate WalkingAlienFinalOutputTruncated.x3dv

echo "Commenting out excess ROUTES (no joints present)..."
(~/Downloads/castle-model-viewer-5.3.0-win64-x86_64/castle-model-viewer/castle-model-converter.exe --validate WalkingAlienFinalOutputTruncated.x3dv 2>&1 | grep "not found"|sed 's/" not found//'| sed 's/.*Route destination node name "//'| sort -u | sed 's/\(.*\)/%s\/^\\(.*ROUTE.*\1.*\\)\/# \\1\//'; echo wq) > ex8.cmds
ex WalkingAlienFinalOutputTruncated.x3dv < ex8.cmds

~/Downloads/castle-model-viewer-5.3.0-win64-x86_64/castle-model-viewer/castle-model-viewer.exe WalkingAlienFinalOutputTruncated.x3dv
#npx sunrize@latest WalkingAlienFinalOutputTruncated.x3dv
rm .WalkingAlienFinalOutputTruncated.x3dv.swp
