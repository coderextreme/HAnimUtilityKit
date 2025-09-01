echo "Downloading Walking Alien.gltf..."
curl https://create3000.github.io/media/glTF/Walking%20Alien/textures/InnerMouth_baseColor.jpeg --output textures/InnerMouth_baseColor.jpeg 
curl https://create3000.github.io/media/glTF/Walking%20Alien/textures/EyeSockets_baseColor.jpeg --output textures/EyeSockets_baseColor.jpeg 
curl https://create3000.github.io/media/glTF/Walking%20Alien/textures/SkinHead_baseColor.jpeg --output textures/SkinHead_baseColor.jpeg 
curl https://create3000.github.io/media/glTF/Walking%20Alien/textures/SkinHands_baseColor.jpeg --output textures/SkinHands_baseColor.jpeg 
curl https://create3000.github.io/media/glTF/Walking%20Alien/textures/SkinFeet_baseColor.jpeg --output textures/SkinFeet_baseColor.jpeg 
curl https://create3000.github.io/media/glTF/Walking%20Alien/textures/SkinBody_baseColor.jpeg --output textures/SkinBody_baseColor.jpeg 
curl https://create3000.github.io/media/glTF/Walking%20Alien/scene.bin --output scene.bin 
curl https://create3000.github.io/media/glTF/Walking%20Alien/Walking%20Alien.gltf --output WalkingAlien.gltf 

echo "Converting Walking Alien from .gltf/.bin to .x3d and .x3dv..."
npx x3d-tidy@latest -f 5 -d 5 -i WalkingAlien.gltf -o WalkingAlienX_ITE.x3d
npx x3d-tidy@latest -f 5 -d 5 -i WalkingAlien.gltf -o WalkingAlienX_ITE.x3dv
npx x3d-tidy@latest -f 5 -d 5 -i JoeHAnimKick1a.x3dv -o JoeHAnimKick1a.x3d


echo "Mapping joints and interpolators..."
python runwalkingalienX_ITE.py
python runwalkingman.py
python runconan.py
python runjoe.py
python runjoedemo5.py

echo "Converting Final Output from .x3d to .x3dv..."
npx x3d-tidy@latest -i WalkingAlienFinalOutputX_ITE.x3d -o WalkingAlienFinalOutputX_ITE.x3dv
npx x3d-tidy@latest -i conan_23_Aug2025_interpolators_mapped.x3d -o conan_23_Aug2025_Final.x3dv
npx x3d-tidy@latest -i walking_man_cc_test_interpolators_mapped.x3d -o walking_man_cc_test_Final.x3dv
npx x3d-tidy@latest -i JoeHAnimKick1a_interpolators_mapped.x3d -o JoeHAnimKick1a_Final.x3dv
npx x3d-tidy@latest -i JoeDemo5JoeSkin5_interpolators_mapped.x3d -o JoeDemo5JoeSkin5_Final.x3dv

echo "Touchups before finding validating..."
(echo '%s/PROFILE Interchange/PROFILE Immersive/'; echo g/colorSpaceConversion/d;  echo wq;) > ex1.cmds
ex WalkingAlienFinalOutputX_ITE.x3dv < ex1.cmds

echo "Adding animations..."
cat Animations2.x3dv >> WalkingAlienFinalOutputX_ITE.x3dv
cat Animations2.x3dv >> conan_23_Aug2025_Final.x3dv
cat Animations2.x3dv >> walking_man_cc_test_Final.x3dv
cat Animations2.x3dv >> JoeHAnimKick1a_Final.x3dv
cat Animations2.x3dv >> JoeDemo5JoeSkin5_Final.x3dv

echo "Validating..."
~/Downloads/castle-model-viewer-5.3.0-win64-x86_64/castle-model-viewer/castle-model-converter.exe --validate WalkingAlienFinalOutputX_ITE.x3dv
~/Downloads/castle-model-viewer-5.3.0-win64-x86_64/castle-model-viewer/castle-model-converter.exe --validate conan_23_Aug2025_Final.x3dv
~/Downloads/castle-model-viewer-5.3.0-win64-x86_64/castle-model-viewer/castle-model-converter.exe --validate walking_man_cc_test_Final.x3dv
~/Downloads/castle-model-viewer-5.3.0-win64-x86_64/castle-model-viewer/castle-model-converter.exe --validate JoeHAnimKick1a_Final.x3dv
~/Downloads/castle-model-viewer-5.3.0-win64-x86_64/castle-model-viewer/castle-model-converter.exe --validate JoeDemo5JoeSkin5_Final.x3dv

echo "Commenting out excess ROUTES (no joints present)..."
(~/Downloads/castle-model-viewer-5.3.0-win64-x86_64/castle-model-viewer/castle-model-converter.exe --validate WalkingAlienFinalOutputX_ITE.x3dv 2>&1 | grep "not found"|sed 's/" not found//'| sed 's/.*Route destination node name "//'| sort -u | sed 's/\(.*\)/%s\/^\\(.*ROUTE.*\1.*\\)\/# \\1\//'; echo wq) > ex2.cmds
ex WalkingAlienFinalOutputX_ITE.x3dv < ex2.cmds
(~/Downloads/castle-model-viewer-5.3.0-win64-x86_64/castle-model-viewer/castle-model-converter.exe --validate conan_23_Aug2025_Final.x3dv 2>&1       | grep "not found"|sed 's/" not found//'| sed 's/.*Route destination node name "//'| sort -u | sed 's/\(.*\)/%s\/^\\(.*ROUTE.*\1.*\\)\/# \\1\//'; echo wq) > ex3.cmds
ex conan_23_Aug2025_Final.x3dv < ex3.cmds
(~/Downloads/castle-model-viewer-5.3.0-win64-x86_64/castle-model-viewer/castle-model-converter.exe --validate walking_man_cc_test_Final.x3dv 2>&1    | grep "not found"|sed 's/" not found//'| sed 's/.*Route destination node name "//'| sort -u | sed 's/\(.*\)/%s\/^\\(.*ROUTE.*\1.*\\)\/# \\1\//'; echo wq) > ex4.cmds
ex walking_man_cc_test_Final.x3dv < ex4.cmds
(~/Downloads/castle-model-viewer-5.3.0-win64-x86_64/castle-model-viewer/castle-model-converter.exe --validate JoeHAnimKick1a_Final.x3dv 2>&1    | grep "not found"|sed 's/" not found//'| sed 's/.*Route destination node name "//'| sort -u | sed 's/\(.*\)/%s\/^\\(.*ROUTE.*\1.*\\)\/# \\1\//'; echo wq) > ex5.cmds
ex JoeHAnimKick1a_Final.x3dv < ex5.cmds
(~/Downloads/castle-model-viewer-5.3.0-win64-x86_64/castle-model-viewer/castle-model-converter.exe --validate JoeDemo5JoeSkin5_Final.x3dv 2>&1    | grep "not found"|sed 's/" not found//'| sed 's/.*Route destination node name "//'| sort -u | sed 's/\(.*\)/%s\/^\\(.*ROUTE.*\1.*\\)\/# \\1\//'; echo wq) > ex6.cmds
ex JoeDemo5JoeSkin5_Final.x3dv < ex6.cmds

#npx sunrize@latest JoeHAnimKick1a_Final.x3dv
#npx sunrize@latest walking_man_cc_test_Final.x3dv
#npx sunrize@latest conan_23_Aug2025_Final.x3dv
npx sunrize@latest WalkingAlienFinalOutputX_ITE.x3dv
~/Downloads/castle-model-viewer-5.3.0-win64-x86_64/castle-model-viewer/castle-model-viewer.exe JoeDemo5JoeSkin5_Final.x3dv
~/Downloads/castle-model-viewer-5.3.0-win64-x86_64/castle-model-viewer/castle-model-viewer.exe JoeHAnimKick1a_Final.x3dv
~/Downloads/castle-model-viewer-5.3.0-win64-x86_64/castle-model-viewer/castle-model-viewer.exe walking_man_cc_test_Final.x3dv
~/Downloads/castle-model-viewer-5.3.0-win64-x86_64/castle-model-viewer/castle-model-viewer.exe conan_23_Aug2025_Final.x3dv
#~/Downloads/castle-model-viewer-5.3.0-win64-x86_64/castle-model-viewer/castle-model-viewer.exe WalkingAlienFinalOutputX_ITE.x3dv
rm .WalkingAlienFinalOutputX_ITE.x3dv.swp
rm .conan_23_Aug2025_Final.x3dv.swp
rm .walking_man_cc_test_Final.x3dv.swp
rm .JoeHAnimKick1a_Final.x3dv.swp
rm .JoeDemo5JoeSkin5.x3dv.swp
