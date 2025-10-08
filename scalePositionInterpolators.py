#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import json
import sys
import os
from typing import Optional, List, Tuple, Dict, Any

class Scale:
    def __init__(self):
        self.HUMANOID_ROOT_HEIGHT = 0.8240
        self.scale = (1, 1, 1)
        self.maxx = -100
        self.minx = 100
        self.maxy = -100
        self.miny = 100
        self.maxz = -100
        self.minz = 100

    def parse_float_array(self, value_str: str) -> List[float]:
        """Parse space-separated float values from X3D attribute strings"""
        if not value_str:
            return []
        return [float(x) for x in value_str.strip().split()]

    def format_float_array(self, values: List[float]) -> str:
        """Format float array back to X3D attribute string"""
        return ' '.join(str(v) for v in values)

    def load_x3d_file(self, filename: str) -> ET.ElementTree:
        """Load X3D file and return ElementTree"""
        tree = ET.parse(filename)
        return tree

    def main(self, input_file: str = None, output_file: str = None):
        """Main function - equivalent to main() in JavaScript"""

        # Load X3D file
        tree = self.load_x3d_file(input_file)
        root = tree.getroot()
        
        humanoid = self.traverse_children_scene_graph(root)
        if humanoid is None:
            print("No humanoid found in scene")
            return
        
        print(f"humanoid: {humanoid.tag}")
        print(f"DEF: {humanoid.get('DEF', 'None')}")
        print(f"name: {humanoid.get('name', 'None')}")
        
        # Find skeleton root joint
        skeleton_joints = self.find_skeleton_joints(humanoid)
        root_joint = None
        
        if skeleton_joints:
            root_joint = skeleton_joints[0]  # Assume first joint is root
            
        if root_joint is not None:
            print(f"root joint: {root_joint}")
            center_str = root_joint.get('center', '0 0 0')
            center = self.parse_float_array(center_str)
            print(f"center: {center}")
            
            
            #try:
            scaleHeight = center[1] / self.HUMANOID_ROOT_HEIGHT
            self.scale = (scaleHeight, scaleHeight, scaleHeight)
            print(f"scale (skeleton) is {self.scale}")
            self.transform_node(root, tree)
            #except Exception as e:
            #    print(f"Error: {e}")

        tree.write(output_file, encoding='utf-8', xml_declaration=True)

    def traverse_children_scene_graph(self, parent: ET.Element) -> Optional[ET.Element]:
        """Traverse scene graph children to find HAnimHumanoid"""
        for child in parent:
            humanoid = self.traverse_child_scene_graph(child)
            if humanoid is not None:
                print(f"Unpacking child {child.tag} succeeded")
                return humanoid
            else:
                print(f"Unpacking child {child.tag} failed")
        return None

    def traverse_child_scene_graph(self, child: ET.Element) -> Optional[ET.Element]:
        """Traverse individual child to find HAnimHumanoid"""
        # Check if this is an HAnimHumanoid
        if child.tag.endswith('HAnimHumanoid') or child.tag == 'HAnimHumanoid':
            print(f"Found humanoid: {child.tag}")
            return child
        
        # Recursively search children
        for grandchild in child:
            result = self.traverse_child_scene_graph(grandchild)
            if result is not None:
                return result
        
        return None

    def find_skeleton_joints(self, humanoid: ET.Element) -> List[ET.Element]:
        """Find all HAnimJoint elements in the skeleton"""
        joints = []
        
        # Look for HAnimJoint elements within the humanoid
        for elem in humanoid.iter():
            if elem.tag.endswith('HAnimJoint') or elem.tag == 'HAnimJoint':
                joints.append(elem)
        
        return joints

    def transform_point(self, point: List[float], point_offset: int) -> List[float]:
        """Transform a 3D point with scale"""
        new_point = point.copy()
        
        if point_offset + 2 < len(new_point):
            # Apply scale
            new_point[point_offset] *= self.scale[0] if len(self.scale) > 0 else 1
            new_point[point_offset + 1] *= self.scale[1] if len(self.scale) > 1 else 1
            new_point[point_offset + 2] *= self.scale[2] if len(self.scale) > 2 else 1
        
        return new_point

    def transform_position_interpolator(self, node: ET.Element) -> bool:
        """Transform PositionInterpolator keyValue points"""
        key_value_str = node.get('keyValue', '').replace(',', ' ')
        if not key_value_str:
            return True

        # Parse keyValue - it's a series of 3D points (x1 y1 z1 x2 y2 z2 ...)
        key_values = self.parse_float_array(key_value_str)
        print(f"Transforming PositionInterpolator with keyValues {key_values}")

        # Transform each 3D point
        for i in range(0, len(key_values), 3):
            if i + 2 < len(key_values):
                key_values = self.transform_point(key_values, i)

        # Update the keyValue attribute
        node.set('keyValue', self.format_float_array(key_values))
        print(f"Transformed PositionInterpolator with keyValues {key_values}")
        return True

    def transform_node(self, node: ET.Element, parent_node: ET.Element) -> bool:
        """Transform node and its children - equivalent to transformNode() in JS"""
        node_tag = node.tag
        # print(f"node_tag is {node_tag}")
        # Handle different node types
        if node_tag.endswith('HAnimHumanoid') or node_tag == 'HAnimHumanoid':
            children = list(node)
        elif node_tag.endswith('Scene') or node_tag == 'Scene':
            children = list(node)
        elif node_tag.endswith('HAnimJoint') or node_tag == 'HAnimJoint':
            children = list(node)
        elif node_tag.endswith('HAnimSite') or node_tag == 'HAnimSite':
            children = list(node)
        elif node_tag.endswith('HAnimSegment') or node_tag == 'HAnimSegment':
            children = list(node)
        elif node_tag.endswith('Group') or node_tag == 'Group':
            children = list(node)
        elif node_tag.endswith('Transform') or node_tag == 'Transform':
            children = list(node)
        elif node_tag.endswith('Shape') or node_tag == 'Shape':
            children = list(node)
        elif node_tag.endswith('Background') or node_tag == 'Background':
            children = list(node)
        elif node_tag.endswith('Text') or node_tag == 'Text':
            children = list(node)
        elif node_tag.endswith('X3D') or node_tag == 'X3D':
            children = list(node)
        elif node_tag.endswith('head') or node_tag == 'head':
            children = list(node)
        elif node_tag.endswith('DirectionalLight') or node_tag == 'DirectionalLight':
            return True
        elif node_tag.endswith('FontStyle') or node_tag == 'FontStyle':
            return True
        elif node_tag.endswith('Inline') or node_tag == 'Inline':
            return True
        elif node_tag.endswith('Normal') or node_tag == 'Normal':
            return True
        elif node_tag.endswith('ProximitySensor') or node_tag == 'ProximitySensor':
            return True
        elif node_tag.endswith('TouchSensor') or node_tag == 'TouchSensor':
            return True
        elif node_tag.endswith('Viewpoint') or node_tag == 'Viewpoint':
            return True
        elif node_tag.endswith('meta') or node_tag == 'meta':
            return True
        elif node_tag.endswith('IndexedFaceSet') or node_tag == 'IndexedFaceSet':
            return True
        elif node_tag.endswith('Coordinate') or node_tag == 'Coordinate':
            ptstr = node.get('point')
            if ptstr is not None:
                points = self.parse_float_array(ptstr.replace(',', ' '))
                for p in range(len(points)):
                    if p % 3 == 0:  # X
                        if self.maxx < points[p]:
                            self.maxx = points[p]
                        if self.minx > points[p]:
                            self.minx = points[p]
                    if p % 3 == 1:  # Y
                        if self.maxy < points[p]:
                            self.maxy = points[p]
                        if self.miny > points[p]:
                            self.miny = points[p]
                    if p % 3 == 2:  # Z
                        if self.maxz < points[p]:
                            self.maxz = points[p]
                        if self.minz > points[p]:
                            self.minz = points[p]
            centerX = (self.maxx+self.minx)/2
            centerY = (self.maxy+self.miny)/2
            centerZ = (self.maxz+self.minz)/2
            scaleX = centerX / self.HUMANOID_ROOT_HEIGHT
            scaleY = centerY / self.HUMANOID_ROOT_HEIGHT
            scaleZ = centerZ / self.HUMANOID_ROOT_HEIGHT
            self.scale = (scaleX, scaleY, scaleZ)
            print(f"scale (Coordinate) is {self.scale}")
            return True
        elif node_tag.endswith('Appearance') or node_tag == 'Appearance':
            return True
        elif node_tag.endswith('PositionInterpolator') or node_tag == 'PositionInterpolator':
            # print(f"PositionInterpolator: {node.keyValue}")
            return self.transform_position_interpolator(node)
        elif node_tag.endswith('OrientationInterpolator') or node_tag == 'OrientationInterpolator':
            return True
        elif node_tag.endswith('ScalarInterpolator') or node_tag == 'ScalarInterpolator':
            return True
        elif node_tag.endswith('CoordinateInterpolator') or node_tag == 'CoordinateInterpolator':
            return True
        elif node_tag.endswith('NormalInterpolator') or node_tag == 'NormalInterpolator':
            return True
        elif node_tag.endswith('TimeSensor') or node_tag == 'TimeSensor':
            return True
        elif node_tag.endswith('ROUTE') or node_tag == 'ROUTE':
            return True
        else:
            if node is not None:
                print(f"Unhandled node: {node_tag}")
            children = list(node)
        
        for child in children:
            if child is not None:
                if not self.transform_node(child, node):
                    print(f"Unpacking child {child.tag} failed")
        
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scalePositionInterpolators.py <input.x3d> [output.x3d]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    humanoid = Scale()
    humanoid.main(input_file, output_file)
