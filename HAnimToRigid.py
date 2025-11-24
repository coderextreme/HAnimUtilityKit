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
        segments = self.root.findall('.//HAnimSegment')
        for segment in segments:
            segment.tag = 'RigidBody'
        parents = self.root.findall('.//HAnimJoint/..')
        for parent_joint in parents:
            xmlstr = xml.etree.ElementTree.tostring(parent_joint, encoding='unicode')
            print(f"{xmlstr}")
            parent_segment = parent_joint.find('RigidBody')
            joints = parent_joint.findall('HAnimJoint')
            for joint in joints:
                segment = joint.find('RigidBody')

                body = xml.etree.ElementTree.SubElement(joint, 'RigidBody')
                body.text = ""
                body.tail = "\n"
                if parent_segment is not None and parent_segment.get("DEF") is not None:
                    body.set("USE", parent_segment.get("DEF"))
                body.set("containerField", "body1")

                body = xml.etree.ElementTree.SubElement(joint, 'RigidBody')
                body.text = ""
                body.tail = "\n"
                if segment is not None and segment.get("DEF") is not None:
                    body.set("USE", segment.get("DEF"))
                body.set("containerField", "body2")
                if segment is not None and segment.get("name") is not None:
                    del segment.attrib["name"]

    def replace_joints(self):
        for joint_parent in self.root.findall('.//HAnimJoint/..'):
            for joint in joint_parent.findall('./HAnimJoint'):
                joint.tag = 'UniversalJoint'
                try:
                    del joint.attrib["name"]
                except KeyError:
                    pass
                # joint.set("containerField", "joints")
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
                route.set("toField", "set_orientation")
                if body is not None and body.get("DEF") is not None:
                    route.set("toNode", body.attrib["DEF"])  # this is the rigid body, but there should only be one TODO

        routes = self.root.findall(".//ROUTE[@toField='set_translation']")
        for route in routes:
            joint = route.attrib['toNode']
            bodies = list(joint)
            bodies = self.root.findall(".//UniversalJoint[@DEF='"+joint+"']/RigidBody")
            for body in bodies:
                route.set("toField", "set_position")
                if body is not None and body.get("DEF") is not None:
                    route.set("toNode", body.attrib["DEF"])  # this is the rigid body, but there should only be one TODO

    def rearrange_hierarchy(self):
            humanoid = self.root.find('.//RigidBodyCollection')
            segments = self.root.findall(".//RigidBody[@DEF]")
            for segment in segments:
                segment.set("containerField", "bodies")
                parent = self.find_parent(segment)
                parent.remove(segment)
                humanoid.append(segment)

            joints = self.root.findall(".//UniversalJoint")
            for joint in joints:
                joint.set("containerField", "joints")
                for child in list(joint):
                    if child.tag == "UniversalJoint":
                        humanoid.append(child)
                        joint.remove(child)

    def cleanup(self):
        humanoids = self.root.findall('.//HAnimHumanoid')
        for humanoid in humanoids:

            segments = humanoid.findall(".//HAnimSegment[@USE]")
            for segment in segments:
                humanoid.remove(segment)

            joints = humanoid.findall(".//HAnimJoint[@USE]")
            for joint in joints:
                humanoid.remove(joint)


    # writeXML.py
    def writeXML(self, OUTPUT_FILE):
        header = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE X3D PUBLIC "ISO//Web3D//DTD X3D 4.0//EN" "https://www.web3d.org/specifications/x3d-4.0.dtd">'
        xmlstr = xml.etree.ElementTree.tostring(self.root, encoding='unicode')
        xmlString = f"{header}{xmlstr}"
        file_output = os.path.join("./",os.path.basename(OUTPUT_FILE))
        with open(file_output, "w") as output_file:
            output_file.write(xmlString)

    def convertDemo5a(self, INPUT_FILE, OUTPUT_FILE):
        self.readXML(INPUT_FILE)
        self.cleanup()
        self.add_component()
        self.replace_humanoids()
        self.replace_segments()
        self.replace_joints()
        self.add_collidable_shapes()
        self.replace_route_fields()
        self.rearrange_hierarchy()
        self.writeXML(OUTPUT_FILE)
