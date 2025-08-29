import xml.etree.ElementTree
import os
import re
import glob
import sys
import time

def rename_interpolators(INPUT_FILE, TIME_SENSORS, OUTPUT_FILE):
    X3D = xml.etree.ElementTree.parse(INPUT_FILE)
    root = X3D.getroot()

    for time_sensor in TIME_SENSORS:
        timer_routes = root.findall(".//ROUTE[@fromNode='"+time_sensor+"'][@fromField='fraction_changed'][@toField='set_fraction']")

        for timer_route in timer_routes:
            expression = timer_route.get("toNode")
            rotation_expression_routes = root.findall(".//ROUTE[@fromNode='"+expression+"'][@fromField='value_changed'][@toField='set_rotation']")
            for rerindex, rotation_expression_route in enumerate(rotation_expression_routes):
                body_part = rotation_expression_route.get("toNode")
                new_orientation_interpolator_name = body_part+"Rotation"+str(rerindex)
                timer_route.set("toNode", new_orientation_interpolator_name)
                rotation_expression_route.set("fromNode", new_orientation_interpolator_name)
                orientation_interpolators = root.findall(".//OrientationInterpolator[@DEF='"+expression+"']")
                for orientation_interpolator in orientation_interpolators:
                    orientation_interpolator.set("DEF", new_orientation_interpolator_name)
                orientation_interpolators = root.findall(".//OrientationInterpolator[@USE='"+expression+"']")
                for orientation_interpolator in orientation_interpolators:
                    orientation_interpolator.set("USE", new_orientation_interpolator_name)

            translation_expression_routes = root.findall(".//ROUTE[@fromNode='"+expression+"'][@fromField='value_changed'][@toField='set_translation']")
            for terindex, translation_expression_route in enumerate(translation_expression_routes):
                body_part = translation_expression_route.get("toNode")
                new_position_interpolator_name = body_part+"Translation"+str(terindex)
                timer_route.set("toNode", new_position_interpolator_name)
                translation_expression_route.set("fromNode", new_position_interpolator_name)
                position_interpolators = root.findall(".//PositionInterpolator[@DEF='"+expression+"']")
                for position_interpolator in position_interpolators:
                    position_interpolator.set("DEF", new_position_interpolator_name)
                position_interpolators = root.findall(".//PositionInterpolator[@USE='"+expression+"']")
                for position_interpolator in position_interpolators:
                    position_interpolator.set("USE", new_position_interpolator_name)

    header = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE X3D PUBLIC "ISO//Web3D//DTD X3D 4.0//EN" "https://www.web3d.org/specifications/x3d-4.0.dtd">'
    xmlstr = xml.etree.ElementTree.tostring(root, encoding='unicode')

    xmlString = f"{header}{xmlstr}"
    file_output = os.path.join("./",os.path.basename(OUTPUT_FILE))
    with open(file_output, "w") as output_file:
        output_file.write(xmlString)
