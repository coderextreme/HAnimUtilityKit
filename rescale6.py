import xml.etree.ElementTree as ET
import argparse
import sys
from typing import List

# --- Helper Functions for X3D Data Types ---

def parse_vec3f(s: str) -> List[float]:
    """
    Parses an SFVec3f string component into a list of 3 floats.
    Handles both space-separated and comma-separated values.
    """
    if not isinstance(s, str):
        return [0.0, 0.0, 0.0]
    try:
        cleaned_s = s.replace(',', ' ')
        return [float(x) for x in cleaned_s.strip().split()]
    except (ValueError, TypeError):
        return [0.0, 0.0, 0.0]

def format_vec3f(v: List[float]) -> str:
    """Formats a list of 3 floats into a standard SFVec3f string."""
    return " ".join(f"{x:.6f}" for x in v)

def parse_mfvec3f(s: str) -> List[List[float]]:
    """
    Parses an MFVec3f string into a list of [x, y, z] lists.
    Handles both space-separated and comma-separated values.
    """
    if not s or not s.strip():
        return []
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
    flat_list = [item for sublist in vectors for item in sublist]
    return " ".join(f"{x:.6f}" for x in flat_list)

# --- Core Logic ---

def process_x3d_file(input_path: str, output_path: str):
    """
    Reads an HAnim X3D file, normalizes its scale to 1 1 1 by baking the
    original scale into the geometry, flattens translations, and writes the result.
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

    humanoid_node = root.find('.//HAnimHumanoid')
    if humanoid_node is None:
        print("Warning: HAnimHumanoid node not found. No action will be taken.", file=sys.stderr)
        tree.write(output_path, encoding="UTF-8", xml_declaration=True)
        return

    original_scale_str = humanoid_node.get('scale', '1 1 1')
    original_scale_vec = parse_vec3f(original_scale_str)
    print(f"Found HAnimHumanoid with original scale: {original_scale_vec}")

    humanoid_node.set('scale', '1 1 1')
    print("Set new HAnimHumanoid scale to: 1 1 1")

    # --- PASS 1: Apply original scaling factor to all relevant attributes ---
    print("\n--- Pass 1: Baking original scale into geometry and animation data... ---")

    mfvec3f_nodes_to_scale = {
        'Coordinate': ['point'],
        'PositionInterpolator': ['keyValue']
    }
    sfvec3f_nodes_to_scale = {
        'Transform': ['translation'],
        'HAnimJoint': ['center', 'translation'], 
        'HAnimSite': ['translation'],
        # Added Group and Shape to scale their bounding box attributes
        'Group': ['bboxCenter', 'bboxSize'],
        'Shape': ['bboxCenter', 'bboxSize']
    }

    for node in root.iter():
        if node.tag in mfvec3f_nodes_to_scale:
            attributes_to_process = mfvec3f_nodes_to_scale[node.tag]
            for attr_name in attributes_to_process:
                if attr_name in node.attrib:
                    points = parse_mfvec3f(node.get(attr_name))
                    scaled_points = [
                        [p[i] * original_scale_vec[i] for i in range(3)]
                        for p in points
                    ]
                    node.set(attr_name, format_mfvec3f(scaled_points))
        
        if node.tag in sfvec3f_nodes_to_scale:
            attributes_to_process = sfvec3f_nodes_to_scale[node.tag]
            for attr_name in attributes_to_process:
                if attr_name in node.attrib:
                    vec = parse_vec3f(node.get(attr_name))
                    scaled_vec = [
                        vec[i] * original_scale_vec[i] for i in range(3)
                    ]
                    node.set(attr_name, format_vec3f(scaled_vec))

    print("Scaling pass completed.")

    # --- PASS 2: Flatten translation hierarchy ---
    print("\n--- Pass 2: Flattening translation hierarchy... ---")

    def flatten_translations_recursive(node: ET.Element, parent_translation: List[float]):
        current_node_translation = [0.0, 0.0, 0.0]
        
        is_transform_node = node.tag in ['Transform', 'HAnimSite']
        if is_transform_node and 'translation' in node.attrib:
            current_node_translation = parse_vec3f(node.get('translation'))

        cumulative_translation_for_children = [
            parent_translation[i] + current_node_translation[i] for i in range(3)
        ]

        for child in node:
            flatten_translations_recursive(child, cumulative_translation_for_children)

        if node.tag == 'Shape':
            coord_node = node.find('Coordinate')
            if coord_node is not None and 'point' in coord_node.attrib:
                points = parse_mfvec3f(coord_node.get('point'))
                translated_points = [
                    [p[i] + cumulative_translation_for_children[i] for i in range(3)]
                    for p in points
                ]
                coord_node.set('point', format_mfvec3f(translated_points))
        
        if is_transform_node and 'translation' in node.attrib:
            node.set('translation', '0 0 0')

    scene_node = root.find('Scene')
    if scene_node:
        flatten_translations_recursive(scene_node, [0.0, 0.0, 0.0])
        print("Flattening pass completed.")
    else:
        print("Warning: <Scene> node not found. Cannot perform translation flattening.", file=sys.stderr)

    try:
        tree.write(output_path, encoding="UTF-8", xml_declaration=True)
        print(f"\nSuccessfully wrote modified HAnim X3D to '{output_path}'")
    except IOError as e:
        print(f"Error: Could not write to output file '{output_path}'. {e}", file=sys.stderr)
        sys.exit(1)

# --- Command-Line Interface ---

def main():
    parser = argparse.ArgumentParser(
        description="Normalize an HAnim X3D file's scale to 1 1 1 and flatten its translation hierarchy.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("input_file", help="Path to the input HAnim X3D (.x3d) file.")
    parser.add_argument("output_file", help="Path to write the modified X3D (.x3d) file.")
    
    args = parser.parse_args()
    process_x3d_file(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
