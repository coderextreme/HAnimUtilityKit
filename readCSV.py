import csv

def readJoints():
    with open('hanim2_loa4_rigidbody_joint_mapping.csv', mode='r', encoding='utf-8') as file:
        joint_reader = csv.DictReader(file)
        joint_map = {}
        for joint in joint_reader:
            joint_map[joint['hanim_joint_name']] = joint['x3d_rbp_joint_node']
        return joint_map

jm = readJoints()
print(jm)
