curl https://create3000.github.io/media/glTF/Walking%20Alien/textures/InnerMouth_baseColor.jpeg --output textures/InnerMouth_baseColor.jpeg 
curl https://create3000.github.io/media/glTF/Walking%20Alien/textures/EyeSockets_baseColor.jpeg --output textures/EyeSockets_baseColor.jpeg 
curl https://create3000.github.io/media/glTF/Walking%20Alien/textures/SkinHead_baseColor.jpeg --output textures/SkinHead_baseColor.jpeg 
curl https://create3000.github.io/media/glTF/Walking%20Alien/textures/SkinHands_baseColor.jpeg --output textures/SkinHands_baseColor.jpeg 
curl https://create3000.github.io/media/glTF/Walking%20Alien/textures/SkinFeet_baseColor.jpeg --output textures/SkinFeet_baseColor.jpeg 
curl https://create3000.github.io/media/glTF/Walking%20Alien/textures/SkinBody_baseColor.jpeg --output textures/SkinBody_baseColor.jpeg 
curl https://create3000.github.io/media/glTF/Walking%20Alien/scene.bin --output scene.bin 
curl https://create3000.github.io/media/glTF/Walking%20Alien/Walking%20Alien.gltf --output WalkingAlien.gltf 

npx x3d-tidy@latest -f 5 -d 5 -i WalkingAlien.gltf -o WalkingAlienX_ITE.x3d
npx x3d-tidy@latest -f 5 -d 5 -i WalkingAlien.gltf -o WalkingAlienX_ITE.x3dv
python runwalkingalienX_ITE.py
npx x3d-tidy@latest -i WalkingAlienFinalOutputX_ITE.x3d -o WalkingAlienFinalOutputX_ITE.x3dv
npx sunrize@latest WalkingAlienFinalOutputX_ITE.x3dv
