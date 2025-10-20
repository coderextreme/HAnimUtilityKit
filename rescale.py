#!/usr/bin/env python3
"""
Python conversion of rescale.js - HAnim humanoid rescaling for X3D files
Converts GraalJS X3D manipulation to Python using ElementTree
"""

import xml.etree.ElementTree as ET
import json
import sys
import os
from typing import Optional, List, Tuple, Dict, Any

# Global variables (matching the original JavaScript)
HUMANCHILD = 3
height = 1.87
scaledHeight = 0
x = 0
miny = 0
l_x = 0
l_z = 0
r_x = 0
r_z = 0
maxy = 0
z = 0
yscale = 1

# HAnim joint name constants
class HAnimJointNames:
    HUMANOID_ROOT = "humanoid_root"
    L_TARSAL_DISTAL_INTERPHALANGEAL_5 = "l_tarsal_distal_interphalangeal_5"
    R_TARSAL_DISTAL_INTERPHALANGEAL_5 = "r_tarsal_distal_interphalangeal_5"

def parse_float_array(value_str: str) -> List[float]:
    """Parse space-separated float values from X3D attribute strings"""
    if not value_str:
        return []
    return [float(x) for x in value_str.strip().split()]

def format_float_array(values: List[float]) -> str:
    """Format float array back to X3D attribute string"""
    return ' '.join(str(v) for v in values)

def get_element_by_def(root: ET.Element, def_name: str) -> Optional[ET.Element]:
    """Find element by DEF attribute"""
    for elem in root.iter():
        if elem.get('DEF') == def_name:
            return elem
    return None

def load_x3d_file(filename: str) -> ET.ElementTree:
    """Load X3D file and return ElementTree"""
    tree = ET.parse(filename)
    return tree

def main(input_file: str = None, output_file: str = None):
    """Main function - equivalent to main() in JavaScript"""
    global HUMANCHILD, height, scaledHeight, x, miny, l_x, l_z, r_x, r_z, maxy, z, yscale
    
    # Reset global variables
    HUMANCHILD = 3
    height = 1.87
    scaledHeight = 0
    x = 0
    miny = 0
    l_x = 0
    l_z = 0
    r_x = 0
    r_z = 0
    maxy = 0
    z = 0
    yscale = 1
    
    if not input_file:
        print("Please provide input X3D file")
        return
    
    # Load X3D file
    tree = load_x3d_file(input_file)
    root = tree.getroot()
    
    count = 0
    humanoid = traverse_children_scene_graph(root)
    count += 1
    
    if humanoid is None:
        print("No humanoid found in scene")
        return
    
    print(f"humanoid: {humanoid.tag}")
    print(f"DEF: {humanoid.get('DEF', 'None')}")
    print(f"name: {humanoid.get('name', 'None')}")
    
    # Get and reset scale
    scale_str = humanoid.get('scale', '1 1 1')
    scale = parse_float_array(scale_str)
    print(f"scale: {scale}")
    
    # Set scale to [1, 1, 1]
    humanoid.set('scale', '1 1 1')
    print(f"scale output: [1, 1, 1]")
    
    # Find skeleton root joint
    skeleton_joints = find_skeleton_joints(humanoid)
    root_joint = None
    
    if skeleton_joints:
        root_joint = skeleton_joints[0]  # Assume first joint is root
        
    if root_joint is not None:
        print(f"root joint: {root_joint.tag}")
        center_str = root_joint.get('center', '0 0 0')
        center = parse_float_array(center_str)
        print(f"center: {center}")
        
        if len(center) >= 3:
            x = center[0]
            miny = center[1]
            maxy = center[1]
            z = center[2]
        
        translation = [0, 0, 0]
        
        try:
            centering(root_joint)
            x = (l_x + r_x) / 2
            z = (l_z + r_z) / 2
            yscale = maxy - miny
            scaledHeight = yscale * scale[1] if len(scale) > 1 else yscale
            print(f"max y {maxy} min y {miny} yscale {yscale} height {height}")
            transform_node(root_joint, translation, scale, humanoid)
        except Exception as e:
            print(f"Error: {e}")
    else:
        translation = [0, 0, 0]
        transform_node(humanoid, translation, scale, humanoid)
        scale = parse_float_array(humanoid.get('scale', '1 1 1'))
        print(f"scale: {scale}")
        
        # Transform scene
        scene = root.find('.//{http://www.web3d.org/specifications/x3d-namespace}Scene') or root.find('.//Scene')
        if scene is not None:
            translation = [0, 0, 0]
            transform_node(scene, translation, scale, tree)
    
    # Save output file
    humanoid_name = humanoid.get('name', 'humanoid') or humanoid.get('DEF', 'humanoid')
    if not output_file:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = f"../data/{humanoid_name}.scaled{count}.x3d"
    
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    print(f"Saved to: {output_file}")

def traverse_children_scene_graph(parent: ET.Element) -> Optional[ET.Element]:
    """Traverse scene graph children to find HAnimHumanoid"""
    for child in parent:
        humanoid = traverse_child_scene_graph(child)
        if humanoid is not None:
            print(f"Unpacking child {child.tag} succeeded")
            return humanoid
        else:
            print(f"Unpacking child {child.tag} failed")
    return None

def traverse_child_scene_graph(child: ET.Element) -> Optional[ET.Element]:
    """Traverse individual child to find HAnimHumanoid"""
    # Check if this is an HAnimHumanoid
    if child.tag.endswith('HAnimHumanoid') or child.tag == 'HAnimHumanoid':
        print(f"Found humanoid: {child.tag}")
        return child
    
    # Recursively search children
    for grandchild in child:
        result = traverse_child_scene_graph(grandchild)
        if result is not None:
            return result
    
    return None

def find_skeleton_joints(humanoid: ET.Element) -> List[ET.Element]:
    """Find all HAnimJoint elements in the skeleton"""
    joints = []
    
    # Look for HAnimJoint elements within the humanoid
    for elem in humanoid.iter():
        if elem.tag.endswith('HAnimJoint') or elem.tag == 'HAnimJoint':
            joints.append(elem)
    
    return joints

def centering(joint: ET.Element):
    """Calculate bounding box and center points - equivalent to centering() in JS"""
    global l_x, l_z, r_x, r_z, miny, maxy
    
    center_str = joint.get('center', '0 0 0')
    center = parse_float_array(center_str)
    name = joint.get('name', '')
    
    if len(center) >= 3:
        # Handle specific joint names
        if name == HAnimJointNames.HUMANOID_ROOT:
            l_x = center[0]
            l_z = center[2]
            r_x = center[0]
            r_z = center[2]
        
        # Update min/max y values
        if center[1] >= maxy:
            maxy = center[1]
        if center[1] <= miny:
            miny = center[1]
    
    # Recursively process child joints
    for child in joint:
        if child.tag.endswith('HAnimJoint') or child.tag == 'HAnimJoint':
            centering(child)

def transform_point(point: List[float], point_offset: int, translation: List[float], scale: List[float]) -> List[float]:
    """Transform a 3D point with translation and scale"""
    new_point = point.copy()
    
    if point_offset + 2 < len(new_point):
        # Apply translation
        new_point[point_offset] += translation[0]
        new_point[point_offset + 1] += translation[1]
        new_point[point_offset + 2] += translation[2]
        
        # Apply scale
        new_point[point_offset] *= scale[0] if len(scale) > 0 else 1
        new_point[point_offset + 1] *= scale[1] if len(scale) > 1 else 1
        new_point[point_offset + 2] *= scale[2] if len(scale) > 2 else 1
    
    return new_point

def transform_position_interpolator(node: ET.Element, translation: List[float], scale: List[float]) -> bool:
    """Transform PositionInterpolator keyValue points"""
    key_value_str = node.get('keyValue', '')
    if not key_value_str:
        return True

    # Parse keyValue - it's a series of 3D points (x1 y1 z1 x2 y2 z2 ...)
    key_values = parse_float_array(key_value_str)

    # Transform each 3D point
    for i in range(0, len(key_values), 3):
        if i + 2 < len(key_values):
            key_values = transform_point(key_values, i, translation, scale)

    # Update the keyValue attribute
    node.set('keyValue', format_float_array(key_values))
    print(f"Transformed PositionInterpolator with {len(key_values)//3} keyframes")
    return True

def transform_orientation_interpolator(node: ET.Element, translation: List[float], scale: List[float]) -> bool:
    """Transform OrientationInterpolator - typically no scaling needed for rotations"""
    # OrientationInterpolator keyValues are axis-angle rotations (x y z angle)
    # Rotations generally don't need scaling, but you might want to transform
    # the rotation axis if the coordinate system changes significantly

    key_value_str = node.get('keyValue', '')
    if not key_value_str:
        return True

    key_values = parse_float_array(key_value_str)

    # Each keyValue is 4 floats: x y z angle
    # For most cases, we don't scale rotations, but log for debugging
    print(f"Found OrientationInterpolator with {len(key_values)//4} keyframes (not scaled)")
    return True

def transform_scalar_interpolator(node: ET.Element, translation: List[float], scale: List[float]) -> bool:
    """Transform ScalarInterpolator - may need scaling depending on what it animates"""
    key_value_str = node.get('keyValue', '')
    if not key_value_str:
        return True

    # ScalarInterpolator keyValues are single float values
    # Whether to scale these depends on what they're animating
    # For size/length values, you'd want to scale; for transparency/rotation, you wouldn't

    print(f"Found ScalarInterpolator (scaling depends on usage context)")
    return True

def transform_coordinate_interpolator(node: ET.Element, translation: List[float], scale: List[float]) -> bool:
    """Transform CoordinateInterpolator keyValue points"""
    key_value_str = node.get('keyValue', '')
    if not key_value_str:
        return True

    # CoordinateInterpolator keyValues are sequences of 3D coordinate sets
    # Each keyframe contains ALL the vertices for that frame
    key_values = parse_float_array(key_value_str)

    # Transform each 3D point
    for i in range(0, len(key_values), 3):
        if i + 2 < len(key_values):
            key_values = transform_point(key_values, i, translation, scale)

    node.set('keyValue', format_float_array(key_values))
    print(f"Transformed CoordinateInterpolator with {len(key_values)//3} vertices")
    return True

def transform_normal_interpolator(node: ET.Element, translation: List[float], scale: List[float]) -> bool:
    """Transform NormalInterpolator - normals need special handling"""
    key_value_str = node.get('keyValue', '')
    if not key_value_str:
        return True

    key_values = parse_float_array(key_value_str)

    # Normals should be normalized after transformation
    # and only rotated, not translated or non-uniformly scaled
    for i in range(0, len(key_values), 3):
        if i + 2 < len(key_values):
            # For normals, we typically only apply rotation part of transformation
            # and ensure they remain unit vectors
            # This is a simplified approach - you may need more sophisticated normal transformation
            normal = [key_values[i], key_values[i+1], key_values[i+2]]

            # Apply only uniform scaling to normals (if scale is uniform)
            if len(scale) >= 3 and abs(scale[0] - scale[1]) < 0.001 and abs(scale[1] - scale[2]) < 0.001:
                # Uniform scale - just normalize after
                length = (normal[0]**2 + normal[1]**2 + normal[2]**2)**0.5
                if length > 0:
                    key_values[i] = normal[0] / length
                    key_values[i+1] = normal[1] / length
                    key_values[i+2] = normal[2] / length

    node.set('keyValue', format_float_array(key_values))
    print(f"Transformed NormalInterpolator with {len(key_values)//3} normals")
    return True

def transform_node(node: ET.Element, parent_translation: List[float], scale: List[float], parent_node: ET.Element) -> bool:
    """Transform node and its children - equivalent to transformNode() in JS"""
    stored_translation = parent_translation.copy()
    
    node_tag = node.tag
    
    # Handle different node types
    if node_tag.endswith('HAnimHumanoid') or node_tag == 'HAnimHumanoid':
        # Process skin children
        children = list(node)
        
    elif node_tag.endswith('Scene') or node_tag == 'Scene':
        children = list(node)
        
    elif node_tag.endswith('HAnimJoint') or node_tag == 'HAnimJoint':
        # Handle joint transformation
        translation_str = node.get('translation', '0 0 0')
        translation = parse_float_array(translation_str)
        
        if len(translation) >= 3:
            stored_translation[0] += translation[0]
            stored_translation[1] += translation[1]
            stored_translation[2] += translation[2]
        
        # Transform center
        center_str = node.get('center', '0 0 0')
        center = parse_float_array(center_str)
        if len(center) >= 3:
            center = transform_point(center, 0, stored_translation, scale)
            node.set('center', format_float_array(center))
        
        # Reset translation
        node.set('translation', '0 0 0')
        children = list(node)
        
    elif node_tag.endswith('HAnimSite') or node_tag == 'HAnimSite':
        # Handle site transformation
        translation_str = node.get('translation', '0 0 0')
        translation = parse_float_array(translation_str)
        
        if len(translation) >= 3:
            stored_translation[0] += translation[0]
            stored_translation[1] += translation[1]
            stored_translation[2] += translation[2]
        
        # Transform center
        center_str = node.get('center', '0 0 0')
        center = parse_float_array(center_str)
        if len(center) >= 3:
            center = transform_point(center, 0, stored_translation, scale)
            node.set('center', format_float_array(center))
        
        # Reset translation
        node.set('translation', '0 0 0')
        children = list(node)
        
    elif node_tag.endswith('HAnimSegment') or node_tag == 'HAnimSegment':
        # Handle segment - find Coordinate nodes
        coord_nodes = []
        for child in node.iter():
            if child.tag.endswith('Coordinate') or child.tag == 'Coordinate':
                coord_nodes.append(child)
        
        for coord in coord_nodes:
            transform_node(coord, stored_translation, scale, node)
        
        children = list(node)
        
    elif node_tag.endswith('Group') or node_tag == 'Group':
        children = list(node)
        
    elif node_tag.endswith('Transform') or node_tag == 'Transform':
        # Handle Transform node
        translation_str = node.get('translation', '0 0 0')
        translation = parse_float_array(translation_str)
        
        if len(translation) >= 3:
            stored_translation[0] += translation[0]
            stored_translation[1] += translation[1]
            stored_translation[2] += translation[2]
        
        # Reset translation if node has DEF or name
        if node.get('DEF') or node.get('name'):
            node.set('translation', '0 0 0')
            children = list(node)
        else:
            print(f"Would delete transform node under {parent_node.tag}")
            children = list(node)
        
    elif node_tag.endswith('Shape') or node_tag == 'Shape':
        # Handle Shape - process appearance and geometry
        for child in node:
            transform_node(child, stored_translation, scale, node)
        return True
        
    elif node_tag.endswith('IndexedFaceSet') or node_tag == 'IndexedFaceSet':
        # Handle IndexedFaceSet - find and transform Coordinate
        coord_index_str = node.get('coordIndex', '')
        if coord_index_str:
            coord_index = [int(x) for x in coord_index_str.replace(',', ' ').split() if x.strip()]
            if len(coord_index) > 700:
                print(f"coordIndex {len(coord_index)}")
        
        for child in node:
            if child.tag.endswith('Coordinate') or child.tag == 'Coordinate':
                transform_node(child, stored_translation, scale, node)
        return True
        
    elif node_tag.endswith('Coordinate') or node_tag == 'Coordinate':
        # Transform coordinate points
        point_str = node.get('point', '')
        if point_str:
            points = parse_float_array(point_str)
            for i in range(0, len(points), 3):
                points = transform_point(points, i, stored_translation, scale)
            node.set('point', format_float_array(points))
        return True
        
    elif node_tag.endswith('Appearance') or node_tag == 'Appearance':
        return True
        
    elif node_tag.endswith('PositionInterpolator') or node_tag == 'PositionInterpolator':
        return transform_position_interpolator(node, stored_translation, scale)

    elif node_tag.endswith('OrientationInterpolator') or node_tag == 'OrientationInterpolator':
        return transform_orientation_interpolator(node, stored_translation, scale)

    elif node_tag.endswith('ScalarInterpolator') or node_tag == 'ScalarInterpolator':
        return transform_scalar_interpolator(node, stored_translation, scale)

    elif node_tag.endswith('CoordinateInterpolator') or node_tag == 'CoordinateInterpolator':
        return transform_coordinate_interpolator(node, stored_translation, scale)

    elif node_tag.endswith('NormalInterpolator') or node_tag == 'NormalInterpolator':
        return transform_normal_interpolator(node, stored_translation, scale)

    # You should also handle other animation-related nodes:
    elif node_tag.endswith('TimeSensor') or node_tag == 'TimeSensor':
        # TimeSensor typically doesn't need coordinate transformation
        return True

    elif node_tag.endswith('ROUTE') or node_tag == 'ROUTE':
        # ROUTE connections don't need transformation
        return True
    else:
        if node is not None:
            print(f"Unhandled node: {node_tag}")
        children = list(node)
    
    # Process children if they exist
    if 'children' in locals():
        for child in children:
            copy_translation = stored_translation.copy()
            if child is not None:
                if not transform_node(child, copy_translation, scale, node):
                    print(f"Unpacking child {child.tag} failed")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rescale.py <input.x3d> [output.x3d]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    main(input_file, output_file)
