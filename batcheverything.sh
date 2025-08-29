echo "Downloading Walking Alien.gltf..."
curl https://create3000.github.io/media/glTF/Walking%20Alien/textures/InnerMouth_baseColor.jpeg --output textures/InnerMouth_baseColor.jpeg 
curl https://create3000.github.io/media/glTF/Walking%20Alien/textures/EyeSockets_baseColor.jpeg --output textures/EyeSockets_baseColor.jpeg 
curl https://create3000.github.io/media/glTF/Walking%20Alien/textures/SkinHead_baseColor.jpeg --output textures/SkinHead_baseColor.jpeg 
curl https://create3000.github.io/media/glTF/Walking%20Alien/textures/SkinHands_baseColor.jpeg --output textures/SkinHands_baseColor.jpeg 
curl https://create3000.github.io/media/glTF/Walking%20Alien/textures/SkinFeet_baseColor.jpeg --output textures/SkinFeet_baseColor.jpeg 
curl https://create3000.github.io/media/glTF/Walking%20Alien/textures/SkinBody_baseColor.jpeg --output textures/SkinBody_baseColor.jpeg 
curl https://create3000.github.io/media/glTF/Walking%20Alien/scene.bin --output scene.bin 
curl https://create3000.github.io/media/glTF/Walking%20Alien/Walking%20Alien.gltf --output WalkingAlien.gltf 

echo "Converting Walking Alien to .x3d and .x3dv..."
npx x3d-tidy@latest -f 5 -d 5 -i WalkingAlien.gltf -o WalkingAlienX_ITE.x3d
npx x3d-tidy@latest -f 5 -d 5 -i WalkingAlien.gltf -o WalkingAlienX_ITE.x3dv

echo "Mapping joints and interpolators..."
python runwalkingalienX_ITE.py
python runwalkingman.py
echo "Converting Walking Alien Final Output from .x3d to .x3dv..."
npx x3d-tidy@latest -i WalkingAlienFinalOutputX_ITE.x3d -o WalkingAlienFinalOutputX_ITE.x3dv
echo "Touchups before finding validating..."
(echo '%s/PROFILE Interchange/PROFILE Immersive/'; echo g/colorSpaceConversion/d;  echo wq;) > ex1.cmds
ex WalkingAlienFinalOutputX_ITE.x3dv < ex1.cmds
echo "Adding animations..."
cat Animations.x3dv >> WalkingAlienFinalOutputX_ITE.x3dv
echo "Validating..."
~/Downloads/castle-model-viewer-5.3.0-win64-x86_64/castle-model-viewer/castle-model-converter.exe --validate WalkingAlienFinalOutputX_ITE.x3dv
echo "Commenting out excess ROUTES (no joints present)..."
(~/Downloads/castle-model-viewer-5.3.0-win64-x86_64/castle-model-viewer/castle-model-converter.exe --validate WalkingAlienFinalOutputX_ITE.x3dv 2>&1 |grep "not found"|sed 's/" not found//'| sed 's/.*Route destination node name "//'|sort -u| sed 's/\(.*\)/%s\/^\\(.*\1.*\\)\/# \\1\//'; echo wq) > ex2.cmds
ex WalkingAlienFinalOutputX_ITE.x3dv < ex2.cmds
npx sunrize@latest WalkingAlienFinalOutputX_ITE.x3dv
rm .WalkingAlienFinalOutputX_ITE.x3dv.swp
