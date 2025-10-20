import xml.etree.ElementTree
import os

class HAnimUtility:
    def __init__(self):
        self.root = None

    # readXML.py
    def readXML(self, INPUT_FILE):
        X3D = xml.etree.ElementTree.parse(INPUT_FILE)
        self.root = X3D.getroot()

    def getRootFromXML(self, INPUT_FILE):
        eX3D = xml.etree.ElementTree.parse(INPUT_FILE)
        return eX3D.getroot()

    # animation_remove.py
    def animation_remove(self):
        for time_sensor_parent in self.root.findall('.//TimeSensor/..'):
            for time_sensor in time_sensor_parent.findall('TimeSensor'):
                time_sensor_parent.remove(time_sensor)

        for route_parent in self.root.findall('.//ROUTE/..'):
            for route in route_parent.findall('ROUTE'):
                route_parent.remove(route)

        for position_interpolator_parent in self.root.findall('.//PositionInterpolator/..'):
            for position_interpolator in position_interpolator_parent.findall('PositionInterpolator'):
                position_interpolator_parent.remove(position_interpolator)

        for orientation_interpolator_parent in self.root.findall('.//OrientationInterpolator/..'):
            for orientation_interpolator in orientation_interpolator_parent.findall('OrientationInterpolator'):
                orientation_interpolator_parent.remove(orientation_interpolator)

    #joint_binding_remove.py
    def joint_binding_remove(self):
        humanoids = self.root.findall("HAnimHumanoid")
        for humanoid in humanoids:
            humanoid.attrib.pop("jointBindingPositions")
            humanoid.attrib.pop("jointBindingRotations")
            humanoid.attrib.pop("jointBindingScales")

    # rename_interpolators.py
    def rename_interpolators(self, TIME_SENSORS):
        for time_sensor in TIME_SENSORS:
            timer_routes = self.root.findall(".//ROUTE[@fromNode='"+time_sensor+"'][@fromField='fraction_changed'][@toField='set_fraction']")

            for timer_route in timer_routes:
                expression = timer_route.get("toNode")
                rotation_expression_routes = self.root.findall(".//ROUTE[@fromNode='"+expression+"'][@fromField='value_changed'][@toField='set_rotation']")
                for rerindex, rotation_expression_route in enumerate(rotation_expression_routes):
                    body_part = rotation_expression_route.get("toNode")
                    new_orientation_interpolator_name = body_part+"Rotation"+str(rerindex)
                    timer_route.set("toNode", new_orientation_interpolator_name)
                    rotation_expression_route.set("fromNode", new_orientation_interpolator_name)
                    orientation_interpolators = self.root.findall(".//OrientationInterpolator[@DEF='"+expression+"']")
                    for orientation_interpolator in orientation_interpolators:
                        orientation_interpolator.set("DEF", new_orientation_interpolator_name)
                    orientation_interpolators = self.root.findall(".//OrientationInterpolator[@USE='"+expression+"']")
                    for orientation_interpolator in orientation_interpolators:
                        orientation_interpolator.set("USE", new_orientation_interpolator_name)

                translation_expression_routes = self.root.findall(".//ROUTE[@fromNode='"+expression+"'][@fromField='value_changed'][@toField='set_translation']")
                for terindex, translation_expression_route in enumerate(translation_expression_routes):
                    body_part = translation_expression_route.get("toNode")
                    new_position_interpolator_name = body_part+"Translation"+str(terindex)
                    timer_route.set("toNode", new_position_interpolator_name)
                    translation_expression_route.set("fromNode", new_position_interpolator_name)
                    position_interpolators = self.root.findall(".//PositionInterpolator[@DEF='"+expression+"']")
                    for position_interpolator in position_interpolators:
                        position_interpolator.set("DEF", new_position_interpolator_name)
                    position_interpolators = self.root.findall(".//PositionInterpolator[@USE='"+expression+"']")
                    for position_interpolator in position_interpolators:
                        position_interpolator.set("USE", new_position_interpolator_name)

    # tangent_remove.py
    def tangent_remove(self):
        for tangent_parent in self.root.findall('.//Tangent/..'):
            for tangent in tangent_parent.findall('Tangent'):
                tangent_parent.remove(tangent)

    # group_remove.py
    def group_remove(self):
        for group_parent in self.root.findall(".//Group[@DEF='AnimationSelectMenu']/.."):
            for group in group_parent.findall("Group[@DEF='AnimationSelectMenu']"):
                group_parent.remove(group)
        for group_parent in self.root.findall(".//Group[@DEF='Interface']/.."):
            for group in group_parent.findall("Group[@DEF='Interface']"):
                group_parent.remove(group)

    # translation_to_center.py
    def swap_translation_center(self, parent_joint, parent_translation):
        child_joints = parent_joint.findall('HAnimJoint')
        for child_joint in child_joints:
            child_translation = child_joint.get("translation", "0 0 0")
            print(f"child {child_joint.get('DEF')} {child_translation}")
            translationp = [float(val) for val in parent_translation.split()]
            translationc = [float(val) for val in child_translation.split()]

            sum_translation = [a + b for a, b in zip(translationp, translationc)]

            summed_translation = ' '.join(map(str, sum_translation))
            child_joint.set("center", summed_translation)
            child_joint.set("translation", "0 0 0")
            child_joint.set("rotation", "0 1 0 0")
            self.swap_translation_center(child_joint, summed_translation)

    # see above
    def translation_to_center(self):
        parent_joints = self.root.findall(".//HAnimHumanoid/HAnimJoint")
        for parent_joint in parent_joints:
            if parent_joint.get('DEF'):
                joint_translation = parent_joint.get("translation", "0 0 0")
                print(f"joint {parent_joint.get('DEF')} {joint_translation}")
                parent_joint.set("center", joint_translation)
                parent_joint.set("translation", "0 0 0")
                parent_joint.set("rotation", "0 1 0 0")
                self.swap_translation_center(parent_joint, joint_translation)
    # writeXML.py
    def writeXML(self, OUTPUT_FILE):
        # TODO remove to use Animations3.x3dv
        self.merge_animations_and_menu("Animations4.x3d", "menu.x3d")
        header = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE X3D PUBLIC "ISO//Web3D//DTD X3D 4.0//EN" "https://www.web3d.org/specifications/x3d-4.0.dtd">'
        xmlstr = xml.etree.ElementTree.tostring(self.root, encoding='unicode')
        xmlString = f"{header}{xmlstr}"
        file_output = os.path.join("./",os.path.basename(OUTPUT_FILE))
        with open(file_output, "w") as output_file:
            output_file.write(xmlString)

    # jointmapper.py, rootmapper.py
    def map_joints(self, skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX):
        sorted_skeleton_map = sorted(skeleton_map_list, key=lambda x: len(x[0]), reverse=True)

        for cc_name, v2_name in sorted_skeleton_map:

            # prepend something to the Joint for DEF

            prepended_joint = OUTPUT_PREFIX+v2_name

            def_joints = self.root.findall(".//HAnimJoint[@DEF='"+cc_name+"']")
            for def_joint in def_joints:
                def_joint_name = def_joint.get("DEF")
                if def_joint_name == cc_name:
                    def_joint.set("DEF", prepended_joint)
                    def_joint.set("name", v2_name)
                # ROUTEs don't have USE
                rotation_joint_routes = self.root.findall(".//ROUTE[@toNode='"+def_joint_name+"'][@toField='set_rotation']")
                for rotation_joint_route in rotation_joint_routes:
                    rotation_joint_route.set("toNode", prepended_joint)
                translation_joint_routes = self.root.findall(".//ROUTE[@toNode='"+def_joint_name+"'][@toField='set_translation']")
                for translation_joint_route in translation_joint_routes:
                    translation_joint_route.set("toNode", prepended_joint)

            use_joints = self.root.findall(".//HAnimJoint[@USE='"+cc_name+"']")
            for use_joint in use_joints:
                use_joint_name = use_joint.get("USE")
                if use_joint_name == cc_name:
                    use_joint.set("USE", prepended_joint)

    def humanoid_replace(self):
        template_root = self.getRootFromXML("JoeDemo5JoeSkin5a.x3d")
        for humanoids_parent in self.root.findall('.//HAnimHumanoid/..'):
            for humanoid in humanoids_parent.findall('HAnimHumanoid'):
                for template_parent in template_root.findall('.//HAnimHumanoid/..'):
                    for template_humanoid in template_parent.findall('HAnimHumanoid'):
                        index = list(template_parent).index(template_humanoid)
                        template_parent.remove(template_humanoid)
                        template_parent.insert(index, humanoid)
        self.root = template_root


    def merge_animations_and_menu(self, ANIMATIONS_FILE, MENU_FILE):
        self.menu = self.getRootFromXML(MENU_FILE)
        self.animations = self.getRootFromXML(ANIMATIONS_FILE)
        scene = self.root.find(".//Scene")
        animations_scene = self.animations.find(".//Scene")

        layer_set = xml.etree.ElementTree.Element('LayerSet')
        layer_set.text = "\n"
        layer_set.tail = "\n"
        layer_set.set("activeLayer", "1")
        layer_set.set("order", "1, 2")

        # MODEL LAYER
        model_layer = xml.etree.ElementTree.Element('Layer')
        model_layer.text = "\n"
        model_layer.tail = "\n"
        model_layer.set("DEF", "Model")

        # Extract Humanoid from the Scene and add to Model layer
        humanoid_parents = list(self.root.findall('.//HAnimHumanoid/..'))
        for humanoid_parent in humanoid_parents:
            for humanoid in humanoid_parent.findall('HAnimHumanoid'):
                humanoid_parent.remove(humanoid)
                model_layer.append(humanoid)

        layer_set.append(model_layer)

        # MENU LAYER
        menu_layer = xml.etree.ElementTree.Element('Layer')
        menu_layer.text = "\n"
        menu_layer.tail = "\n"
        menu_layer.set("DEF", "Menu")

        viewpoint = xml.etree.ElementTree.Element('Viewpoint')
        viewpoint.text = "\n"
        viewpoint.tail = "\n"
        viewpoint.set("position", "0 20 110")
        menu_layer.append(viewpoint)

        # Add the MenuItem ProtoDeclare (defines the prototype structure)
        menu_layer.append(self.menu.find(".//ProtoDeclare[@name='MenuItem']"))

        # Add the animations group
        menu_layer.append(self.animations.find(".//Group[@DEF='AllAnimations']"))

        # Add all ProtoInstances and their associated routes from the menu
        proto_instances = self.menu.findall(".//ProtoInstance[@name='MenuItem']")
        for proto_instance in proto_instances:
            menu_layer.append(proto_instance)
            proto_def = proto_instance.get("DEF")
            routes = self.menu.findall(f".//Layer/ROUTE[@fromNode='{proto_def}']")
            for route in routes:
                menu_layer.append(route)

        time_sensors = self.animations.findall(".//TimeSensor")
        for time_sensor in time_sensors:
            time_sensor_def = time_sensor.get("DEF")
            routes = animations_scene.findall(f".//ROUTE[@fromNode='{time_sensor_def}']")
            for route in routes:
                animations_scene.remove(route)
                menu_layer.append(route)

        layer_set.append(menu_layer)
        scene.append(layer_set)

    def mix_rename(self, INPUT_FILE, skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX, TIME_SENSORS, FINAL_FILE):
        self.readXML(INPUT_FILE)
        self.animation_remove()
        self.map_joints(skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX)
        #self.joint_binding_remove()
        #self.tangent_remove()
        self.translation_to_center()
        self.writeXML(FINAL_FILE)

    def standard_rename(self, INPUT_FILE, skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX, TIME_SENSORS, FINAL_FILE):
        self.readXML(INPUT_FILE)
        self.animation_remove()
        # self.humanoid_replace()
        self.map_joints(skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX)
        # We removed animations, above.
        # self.rename_interpolators(TIME_SENSORS)
        self.writeXML(FINAL_FILE)

    def joe_rename(self, INPUT_FILE, skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX, TIME_SENSORS, FINAL_FILE):
        self.readXML(INPUT_FILE)
        self.animation_remove()
        # self.humanoid_replace()
        self.map_joints(skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX)
        # We removed animations, above.
        # self.rename_interpolators(TIME_SENSORS)
        self.writeXML(FINAL_FILE)

#    def standard_rename_with_group(self, INPUT_FILE, skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX, TIME_SENSORS, FINAL_FILE):
#        self.readXML(INPUT_FILE)
#        self.animation_remove()
#        # self.humanoid_replace()
#        self.group_remove()
#        self.map_joints(skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX)
#        # We removed animations, above.
#        # self.rename_interpolators(TIME_SENSORS)
#        self.writeXML(FINAL_FILE)

#    # called if you want to maintain existing animations
#    def interpolator_rename(self, INPUT_FILE, skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX, TIME_SENSORS, FINAL_FILE):
#        self.readXML(INPUT_FILE)
#        # animations are not removed
#        # self.humanoid_replace()
#        self.map_joints(skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX)
#        self.rename_interpolators(TIME_SENSORS)
#        self.writeXML(FINAL_FILE)

#    # called after tidy conversion from .gltf and animations truncated
#    def truncated_rename(self, INPUT_FILE, skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX, TIME_SENSORS, FINAL_FILE):
#        self.readXML(INPUT_FILE)
#        # animations were removed by hand
#        # self.animation_remove()
#        # self.humanoid_replace()
#        self.map_joints(skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX)
#        # animations were removed by hand
#        # self.rename_interpolators(root, TIME_SENSORS)
#        self.joint_binding_remove()
#        self.tangent_remove()
#        self.translation_to_center()
#        self.writeXML(FINAL_FILE)

    # called after tidy conversion from .gltf.
    def tidy_rename(self, INPUT_FILE, skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX, TIME_SENSORS, FINAL_FILE):
        self.readXML(INPUT_FILE)
        self.animation_remove()
        # self.humanoid_replace()
        self.map_joints(skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX)
        # We removed animations, above.
        # self.rename_interpolators(root, TIME_SENSORS)
        self.joint_binding_remove()
        self.tangent_remove()
        self.translation_to_center()
        self.writeXML(FINAL_FILE)

    def jin_remove_animations(self, INPUT_FILE, skeleton_map_list, INPUT_PREFIX, OUTPUT_PREFIX, TIME_SENSORS, FINAL_FILE):
        self.readXML(INPUT_FILE)
        self.animation_remove()
        self.group_remove()
        self.writeXML(FINAL_FILE)
