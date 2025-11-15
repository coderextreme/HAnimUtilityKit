import xml.etree.ElementTree
import os

class HAnimToRigid:
    def __init__(self):
        self.root = None

    # readXML.py
    def readXML(self, INPUT_FILE):
        X3D = xml.etree.ElementTree.parse(INPUT_FILE)
        self.root = X3D.getroot()

    def add_component(self):
        component = xml.etree.ElementTree.Element('component')
        component.text = ""
        component.tail = "\n"
        component.set("name", "RigidBodyPhysics")
        component.set("level", "2")
        head = self.root.find('head')
        head.insert(0, component)

    def replace_humanoids(self):
        for humanoid_parent in self.root.findall('.//HAnimHumanoid/..'):
            for humanoid in humanoid_parent.findall('./HAnimHumanoid'):
                humanoid.tag = 'RigidBodyCollection'
                try:
                    del humanoid.attrib["loa"]
                except KeyError:
                    pass
                try:
                    del humanoid.attrib["name"]
                except KeyError:
                    pass
                try:
                    del humanoid.attrib["version"]
                except KeyError:
                    pass

    def replace_segments(self):
        for segment_parent in self.root.findall('.//HAnimSegment/..'):
            for segment in segment_parent.findall('./HAnimSegment'):
                segment.tag = 'RigidBody'
                if segment.get("containerField") == "segments":
                    segment.set("containerField", "bodies")
                else:
                    segment.set("containerField", "body1")  # There's only one body per joint, more later
                try:
                    del segment.attrib["name"]
                except KeyError:
                    pass

    def replace_joints(self):
        for joint_parent in self.root.findall('.//HAnimJoint/..'):
            for joint in joint_parent.findall('./HAnimJoint'):
                joint.tag = 'UniversalJoint'
                try:
                    del joint.attrib["name"]
                except KeyError:
                    pass
                # think about how a joint is in a rigid body collection
                joint.set("containerField", "children")
                try:
                    if joint.attrib["center"]:
                        joint.set("anchorPoint", joint.attrib["center"])
                    del joint.attrib["center"]
                except KeyError:
                    pass

    def find_parent(self, child):
        for parent in self.root.iter():
            if child in parent:
                return parent
        return None

    def add_collidable_shapes(self):
            shapes = self.root.findall(".//UniversalJoint/RigidBody/Shape")
            for shape in shapes:
                parent = self.find_parent(shape)
                collidable_shape = xml.etree.ElementTree.Element('CollidableShape')
                collidable_shape.text = "\n"
                collidable_shape.tail = "\n"
                collidable_shape.set("containerField", "geometry")
                collidable_shape.append(shape)
                shape.set("containerField", "shape")
                parent.append(collidable_shape)
                parent.remove(shape)

    def replace_route_fields(self):
        routes = self.root.findall(".//ROUTE[@toField='set_rotation']")
        for route in routes:
            joint = route.attrib['toNode']
            bodies = list(joint)
            bodies = self.root.findall(".//UniversalJoint[@DEF='"+joint+"']/RigidBody")
            for body in bodies:
                print(f"joint is {joint} body is {body.attrib['DEF']}")
                route.set("toField", "set_orientation")
                route.set("toNode", body.attrib["DEF"])  # this is the rigid body, but there should only be one TODO

        routes = self.root.findall(".//ROUTE[@toField='set_translation']")
        for route in routes:
            joint = route.attrib['toNode']
            bodies = list(joint)
            bodies = self.root.findall(".//UniversalJoint[@DEF='"+joint+"']/RigidBody")
            for body in bodies:
                print(f"joint is {joint} body is {body.attrib['DEF']}")
                route.set("toField", "set_position")
                route.set("toNode", body.attrib["DEF"])  # this is the rigid body, but there should only be one TODO

    # writeXML.py
    def writeXML(self, OUTPUT_FILE):
        # TODO remove to use Animations3.x3dv
        header = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE X3D PUBLIC "ISO//Web3D//DTD X3D 4.0//EN" "https://www.web3d.org/specifications/x3d-4.0.dtd">'
        xmlstr = xml.etree.ElementTree.tostring(self.root, encoding='unicode')
        xmlString = f"{header}{xmlstr}"
        file_output = os.path.join("./",os.path.basename(OUTPUT_FILE))
        with open(file_output, "w") as output_file:
            output_file.write(xmlString)

    def convertDemo5a(self, INPUT_FILE, OUTPUT_FILE):
        self.readXML(INPUT_FILE)
        self.add_component()
        self.replace_humanoids()
        self.replace_segments()
        self.replace_joints()
        self.add_collidable_shapes()
        self.replace_route_fields()
        self.writeXML(OUTPUT_FILE)
