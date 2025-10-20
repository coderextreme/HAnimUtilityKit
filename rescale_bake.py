import xml.etree.ElementTree as ET
import argparse
import sys
from typing import List, Tuple

# This script requires the NumPy library for 3D transformation mathematics.
try:
    import numpy as np
except ImportError:
    print("Error: This script requires the NumPy library.", file=sys.stderr)
    print("Please install it using: pip install numpy", file=sys.stderr)
    sys.exit(1)

# --- Helper Functions for X3D Data Types ---

def parse_vec3f(s: str) -> List[float]:
    """Parses an SFVec3f/SFColor string component into a list of 3 floats."""
    if not isinstance(s, str): return [0.0, 0.0, 0.0]
    try:
        cleaned_s = s.replace(',', ' ')
        return [float(x) for x in cleaned_s.strip().split()]
    except (ValueError, TypeError):
        return [0.0, 0.0, 0.0]

def format_vec3f(v: List[float]) -> str:
    """Formats a list of 3 floats into a standard SFVec3f string."""
    return " ".join(f"{x:.6f}" for x in v)

def parse_rotation(s: str) -> List[float]:
    """Parses an SFRotation (axis-angle) string into a list of 4 floats."""
    if not isinstance(s, str): return [0.0, 0.0, 1.0, 0.0]
    try:
        cleaned_s = s.replace(',', ' ')
        return [float(x) for x in cleaned_s.strip().split()]
    except (ValueError, TypeError):
        return [0.0, 0.0, 1.0, 0.0]

def format_rotation(v: List[float]) -> str:
    """Formats a list of 4 floats into a standard SFRotation string."""
    return " ".join(f"{x:.6f}" for x in v)

def parse_mfvec3f(s: str) -> List[List[float]]:
    """Parses an MFVec3f string into a list of [x, y, z] lists."""
    if not s or not s.strip(): return []
    try:
        cleaned_s = s.replace(',', ' ')
        parts = [float(x) for x in cleaned_s.strip().split()]
        if len(parts) % 3 != 0:
            print(f"Warning: MFVec3f data has an incomplete vector. Length is not a multiple of 3.", file=sys.stderr)
        return [parts[i:i+3] for i in range(0, len(parts) - (len(parts) % 3), 3)]
    except (ValueError, TypeError):
        return []

def format_mfvec3f(vectors: List[List[float]]) -> str:
    """Formats a list of [x, y, z] lists into a standard MFVec3f string."""
    if not vectors: return ""
    flat_list = [item for sublist in vectors for item in sublist]
    return " ".join(f"{x:.6f}" for x in flat_list)

# --- Matrix Helper Functions ---

def axis_angle_to_matrix(axis: np.ndarray, angle: float) -> np.ndarray:
    """Converts an axis-angle rotation to a 4x4 transformation matrix."""
    if np.isclose(angle, 0) or np.linalg.norm(axis) < 1e-6:
        return np.identity(4)
        
    axis = axis / np.linalg.norm(axis)
    c = np.cos(angle)
    s = np.sin(angle)
    t = 1 - c
    x, y, z = axis
    
    rotation_matrix = np.array([
        [t*x*x + c,   t*x*y - s*z, t*x*z + s*y, 0],
        [t*x*y + s*z, t*y*y + c,   t*y*z - s*x, 0],
        [t*x*z - s*y, t*y*z + s*x, t*z*z + c,   0],
        [0,           0,           0,           1]
    ])
    return rotation_matrix

def create_transform_matrix(
    translation: List[float], 
    rotation: List[float], 
    scale: List[float],
    center: List[float],
    scale_orientation: List[float]
) -> np.ndarray:
    """
    Creates a 4x4 transformation matrix from X3D attributes.
    Follows the X3D spec order: T * C * R * SO * S * -SO * -C
    """
    T = np.identity(4)
    T[:3, 3] = translation

    C = np.identity(4)
    C[:3, 3] = center
    inv_C = np.identity(4)
    inv_C[:3, 3] = [-x for x in center]

    R = axis_angle_to_matrix(np.array(rotation[:3]), rotation[3])
    SO = axis_angle_to_matrix(np.array(scale_orientation[:3]), scale_orientation[3])
    inv_SO = SO.T # For rotation matrices, inverse is the transpose

    S = np.diag(scale + [1.0])

    # Compose the final matrix
    # M = T @ C @ R @ SO @ S @ inv_SO @ inv_C
    return T @ C @ R @ SO @ S @ inv_SO @ inv_C

def transform_points(points: List[List[float]], matrix: np.ndarray) -> List[List[float]]:
    """Applies a 4x4 transformation matrix to a list of 3D points."""
    if not points:
        return []
    # Convert points to homogeneous coordinates (x, y, z, 1)
    points_arr = np.array(points)
    homogeneous_points = np.hstack([points_arr, np.ones((points_arr.shape[0], 1))])
    
    # Apply transformation
    transformed_points = (matrix @ homogeneous_points.T).T
    
    # Convert back to 3D coordinates
    return (transformed_points[:, :3] / transformed_points[:, 3, np.newaxis]).tolist()

# --- Core Logic ---

def bake_and_flatten_transforms(node: ET.Element, parent_matrix: np.ndarray):
    """
    Recursively traverses the scene graph, baking transforms into vertices
    and resetting node transformations to identity.
    """
    # 1. Determine the local transformation for the current node
    local_matrix = np.identity(4)
    is_transform_node = node.tag in ['HAnimHumanoid', 'HAnimJoint', 'HAnimSite', 'Transform']

    if is_transform_node:
        translation = parse_vec3f(node.get('translation', '0 0 0'))
        center = parse_vec3f(node.get('center', '0 0 0'))
        rotation = parse_rotation(node.get('rotation', '0 0 1 0'))
        scale = parse_vec3f(node.get('scale', '1 1 1'))
        scale_orientation = parse_rotation(node.get('scaleOrientation', '0 0 1 0'))
        
        local_matrix = create_transform_matrix(translation, rotation, scale, center, scale_orientation)

    # 2. Calculate the cumulative world matrix for this node
    world_matrix = parent_matrix @ local_matrix

    # 3. Apply the world transformation to relevant data in this node's direct children
    # This affects geometry, animation points, and other positional attributes.
    
    # HAnimJoint `center` needs to be transformed
    # TODO Think hard about the next few lines
    if node.tag == 'HAnimJoint':
    # if node.tag == 'HAnimJoint' and 'center' in node.attrib:
        #center_point = parse_vec3f(node.get('center'))
        center_point = parse_vec3f(node.get('translation', '0 0 0'))
        transformed_center = transform_points([center_point], world_matrix)[0]
        node.set('center', format_vec3f(transformed_center))

    if node.tag == 'HAnimHumanoid' and 'jointBindingPositions' in node.attrib:
        jointBindingPositions = parse_mfvec3f(node.get('jointBindingPositions'))
        transformed_positions = transform_points(jointBindingPositions, world_matrix)[0]
        node.set('jointBindingPositions', format_mfvec3f(transformed_positions))

    if node.tag == 'HAnimHumanoid' and 'jointBindingScales' in node.attrib:
        jointBindingScales = parse_mfvec3f(node.get('jointBindingScales'))
        transformed_scales = transform_points(jointBindingScales, world_matrix)[0]
        node.set('jointBindingScales', format_mfvec3f(transformed_scales))

    # Geometry inside a Shape node
    shape_node = node.find('Shape')
    if shape_node is not None:
        coord_node = shape_node.find('Coordinate')
        if coord_node and 'point' in coord_node.attrib:
            points = parse_mfvec3f(coord_node.get('point'))
            transformed_points = transform_points(points, world_matrix)
            coord_node.set('point', format_mfvec3f(transformed_points))

    # PositionInterpolator key values
    pos_interpolator_nodes = node.findall('PositionInterpolator')
    for pi_node in pos_interpolator_nodes:
        if 'keyValue' in pi_node.attrib:
            key_values = parse_mfvec3f(pi_node.get('keyValue'))
            transformed_key_values = transform_points(key_values, world_matrix)
            pi_node.set('keyValue', format_mfvec3f(transformed_key_values))
    
    # Note: OrientationInterpolator `keyValue` is not modified. Those are local
    # rotations that should be preserved for animation.

    # 4. Recurse to children, passing down the new cumulative world matrix
    for child in node:
        bake_and_flatten_transforms(child, world_matrix)

    # 5. After children are processed, reset this node's transformations.
    # This "flattens" the hierarchy. We keep `center` as it's part of the
    # joint's definition, now in world space.
    if is_transform_node:
        if 'translation' in node.attrib: node.set('translation', '0 0 0')
        if 'rotation' in node.attrib: node.set('rotation', '0 0 1 0')
        if 'scale' in node.attrib: node.set('scale', '1 1 1')
        if 'scaleOrientation' in node.attrib: node.set('scaleOrientation', '0 0 1 0')


def process_x3d_file(input_path: str, output_path: str):
    """
    Reads an HAnim X3D file, bakes all hierarchical scale, rotation, and
    translation transforms into the geometry, and writes the flattened result.
    """
    print(f"Processing '{input_path}'...")

    try:
        tree = ET.parse(input_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error: Could not parse XML file. {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_path}'", file=sys.stderr)
        sys.exit(1)

    scene_node = root.find('Scene')
    if scene_node is None:
        print("Error: <Scene> node not found. Cannot process the file.", file=sys.stderr)
        sys.exit(1)

    print("Baking hierarchical transformations into geometry...")
    
    # Start the recursive process from the Scene node with an identity matrix
    initial_matrix = np.identity(4)
    bake_and_flatten_transforms(scene_node, initial_matrix)
    
    print("Transformation baking and hierarchy flattening complete.")

    try:
        tree.write(output_path, encoding="UTF-8", xml_declaration=True)
        print(f"\nSuccessfully wrote modified HAnim X3D to '{output_path}'")
    except IOError as e:
        print(f"Error: Could not write to output file '{output_path}'. {e}", file=sys.stderr)
        sys.exit(1)

# --- Command-Line Interface ---

def main():
    parser = argparse.ArgumentParser(
        description="Bakes hierarchical scale, rotation, and translation transforms in an HAnim X3D file into its geometry, flattening the transform hierarchy.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="This tool requires the NumPy library (pip install numpy)."
    )
    parser.add_argument("input_file", help="Path to the input HAnim X3D (.x3d) file.")
    parser.add_argument("output_file", help="Path to write the modified X3D (.x3d) file.")
    
    args = parser.parse_args()
    process_x3d_file(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
