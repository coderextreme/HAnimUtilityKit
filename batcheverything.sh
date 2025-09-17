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
#npx x3d-tidy@latest -f 5 -d 5 -i WalkingAlien.gltf -o WalkingAlien.x3d
#npx x3d-tidy@latest -f 5 -d 5 -i WalkingAlien.gltf -o WalkingAlien.x3dv
npx x3d-tidy@latest -f 5 -d 5 -i JoeHAnimKick1a.x3dv -o JoeHAnimKick1a.x3d

#cp walking_man_cc_test.new.python.x3d walking_man_cc_test.x3d
#cp conan_23_Aug2025.x3d conan_23_Aug2025.scaled.x3d
#cp WalkingAlien.x3d WalkingAlien.scaled.x3d
python rescale6.py walking_man_cc_test.new.python.x3d walking_man_cc_test.x3d
python rescale6.py conan_23_Aug2025.x3d conan_23_Aug2025.scaled.x3d
python rescale6.py WalkingAlien.x3d WalkingAlien.scaled.x3d


echo "Mapping joints and interpolators..."
python runjin.py
python runwalkingalien.py
python runwalkingman.py
python runconan.py
python runjoe.py
python runjoedemo5.py
# python runjoedemo5a.py

for X3D in JoeHAnimKick1a_Final.x3d JoeDemo5JoeSkin5_Final.x3d conan_23_Aug2025_Final.x3d WalkingAlien_Final.x3d walking_man_cc_test_Final.x3d JinLOA4.scaled1_Final.x3d # JoeDemo5JoeSkin5a_Final.x3d
do
	X3DV="${X3D}v"
	X3DOM=`basename "${X3D}" Final.x3d`x3dom.x3d
	echo "Converting Final Output from .x3d to .x3dv..."
	npx x3d-tidy@latest -i "${X3D}" -o "${X3DV}"

	echo "Touchups before finding validating..."
	(echo '%s/PROFILE Interchange/PROFILE Immersive/'; echo g/colorSpaceConversion/d;  echo wq;) > "${X3DV}".cmds
	ex "${X3DV}"  < "${X3DV}".cmds

	#if [[ $a != Joe* ]]
	#then
		echo "Adding animations..."
		cat Animations3.x3dv >> "${X3DV}"
	#fi

	echo "Validating..."
	~/Downloads/castle-model-viewer-5.3.0-win64-x86_64/castle-model-viewer/castle-model-converter.exe --validate "${X3DV}" 2>&1 | sort -u

	echo "Commenting out excess ROUTES (no joints present)..."
	(~/Downloads/castle-model-viewer-5.3.0-win64-x86_64/castle-model-viewer/castle-model-converter.exe --validate "${X3DV}" 2>&1 | grep "castle-model-converter: Warning: X3D: Route destination node name .* not found" |sed 's/" not found//'| sed 's/.*Route destination node name "//'| sort -u | sed 's/\(.*\)/%s\/^\\(.*ROUTE.*\1.*\\)\/# \\1\//'; echo wq) > "${X3DV}".cmds
	ex "${X3DV}" < "${X3DV}".cmds

	npx sunrize@latest "${X3DV}"
	~/Downloads/castle-model-viewer-5.3.0-win64-x86_64/castle-model-viewer/castle-model-viewer.exe "${X3DV}"
	echo npx x3d-tidy@latest -i "${X3DV}" -o "${X3DOM}"
	npx x3d-tidy@latest -i "${X3DV}" -o "${X3DOM}"
	rm -f ."${X3DV}".swp
	rm -f "${X3DV}".cmds
done
