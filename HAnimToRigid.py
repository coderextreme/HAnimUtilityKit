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
            #xmlstr = xml.etree.ElementTree.tostring(parent_joint, encoding='unicode')
            #print(f"{xmlstr}")
            parent_segments = parent_joint.findall('RigidBody')
            for parent_segment in parent_segments:  # there should be only one
                joints = parent_joint.findall('HAnimJoint')
                for joint in joints:
                    segments = joint.findall('RigidBody')  # one segment per joint
                    for segment in segments:
                        if parent_segment is not None and parent_segment.get("DEF") is not None:
                            joint.set("body1", parent_segment.get("DEF"))
                            # parent_segment.set("containerField", "body1")
                            print(f"found parent segment {parent_segment.get('DEF')} def for {segment.get('DEF')}")
                        elif parent_segment is None:
                            print(f"no parent segment")
                        else:
                            print(f"found parent segment, DEF is None")
                        if segment.get("DEF") is not None:
                            joint.set("body2", segment.get("DEF"))
                            # segment.set("containerField", "body2")
                        try:
                            del segment.attrib["name"]
                        except KeyError:
                            pass
                        if joint.get('body1') is None:
                            try:
                                del joint.attrib["body2"]  # remove body2 if body1 isn't present
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

    def rearrange_hierarchy(self):
            humanoid = self.root.find('.//RigidBodyCollection')
            segments = self.root.findall(".//RigidBody")
            for segment in segments:
                segment.set("containerField", "bodies")
                parent = self.find_parent(segment)
                parent.remove(segment)
                humanoid.append(segment)

            joints = self.root.findall(".//UniversalJoint")
            for joint in joints:
                joint.set("containerField", "joints")
                for child in list(joint):
                    humanoid.append(child)
                    joint.remove(child)

    def cleanup(self):
        humanoids = self.root.findall('.//RigidBodyCollection')
        for humanoid in humanoids:
            segments = humanoid.findall(".//RigidBody[@USE]")
            for segment in segments:
                humanoid.remove(segment)
            joints = humanoid.findall(".//UniversalJoint[@USE]")
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
        self.add_component()
        self.replace_humanoids()
        self.replace_segments()
        self.replace_joints()
        self.add_collidable_shapes()
        self.replace_route_fields()
        self.rearrange_hierarchy()
        self.cleanup()
        self.writeXML(OUTPUT_FILE)
