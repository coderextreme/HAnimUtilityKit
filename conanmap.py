# Mapping from Conan game skeleton joints to Humanoid4 anatomical joints
# Format: (conan_joint, humanoid4_joint)

skeleton_map_list = [
    # Root and spine
    ("GameSkeletonRoot_M", "humanoid_root"),
    ("GameSkeletonSpine1_M", "vl5"),
    ("GameSkeletonChest_M", "vt12"),
    ("GameSkeletonNeck_M", "vc7"),
    ("GameSkeletonNeckPart1_M", "vc6"),
    ("GameSkeletonNeckPart2_M", "vc5"),
    
    # Head
    ("GameSkeletonHead_M", "skullbase"),
    ("GameSkeletonJawJoint_M", "temporomandibular"),
    
    # Eyes
    ("GameSkeletonEyeJoint_L", "l_eyeball_joint"),
    ("GameSkeletonEyeJoint_R", "r_eyeball_joint"),
    
    # Eyebrows
    ("GameSkeletonEyeBrowMid1Joint_L", "l_eyebrow_joint"),
    ("GameSkeletonEyeBrowMid1Joint_R", "r_eyebrow_joint"),
    
    # Eyelids
    ("GameSkeletonupperLidMain0_L", "l_eyelid_joint"),
    ("GameSkeletonupperLidMain0_R", "r_eyelid_joint"),
    
    # Arms - Left
    ("GameSkeletonScapula_L", "l_sternoclavicular"),
    ("GameSkeletonShoulder_L", "l_shoulder"),
    ("GameSkeletonShoulderPart1_L", "l_acromioclavicular"),
    ("GameSkeletonElbow_L", "l_elbow"),
    ("GameSkeletonWrist_L", "l_radiocarpal"),
    
    # Arms - Right
    ("GameSkeletonScapula_R", "r_sternoclavicular"),
    ("GameSkeletonShoulder_R", "r_shoulder"),
    ("GameSkeletonShoulderPart1_R", "r_acromioclavicular"),
    ("GameSkeletonElbow_R", "r_elbow"),
    ("GameSkeletonWrist_R", "r_radiocarpal"),
    
    # Left Hand Fingers
    ("GameSkeletonThumbFinger1_L", "l_carpometacarpal_1"),
    ("GameSkeletonThumbFinger2_L", "l_metacarpophalangeal_1"),
    ("GameSkeletonThumbFinger3_L", "l_carpal_interphalangeal_1"),
    
    ("GameSkeletonIndexFinger1_L", "l_carpometacarpal_2"),
    ("GameSkeletonIndexFinger2_L", "l_metacarpophalangeal_2"),
    ("GameSkeletonIndexFinger3_L", "l_carpal_proximal_interphalangeal_2"),
    ("GameSkeletonIndexFinger4_L", "l_carpal_distal_interphalangeal_2"),
    
    ("GameSkeletonMiddleFinger1_L", "l_carpometacarpal_3"),
    ("GameSkeletonMiddleFinger2_L", "l_metacarpophalangeal_3"),
    ("GameSkeletonMiddleFinger3_L", "l_carpal_proximal_interphalangeal_3"),
    ("GameSkeletonMiddleFinger4_L", "l_carpal_distal_interphalangeal_3"),
    
    ("GameSkeletonRingFinger1_L", "l_carpometacarpal_4"),
    ("GameSkeletonRingFinger2_L", "l_metacarpophalangeal_4"),
    ("GameSkeletonRingFinger3_L", "l_carpal_proximal_interphalangeal_4"),
    ("GameSkeletonRingFinger4_L", "l_carpal_distal_interphalangeal_4"),
    
    ("GameSkeletonPinkyFinger1_L", "l_carpometacarpal_5"),
    ("GameSkeletonPinkyFinger2_L", "l_metacarpophalangeal_5"),
    ("GameSkeletonPinkyFinger3_L", "l_carpal_proximal_interphalangeal_5"),
    ("GameSkeletonPinkyFinger4_L", "l_carpal_distal_interphalangeal_5"),
    
    # Right Hand Fingers
    ("GameSkeletonThumbFinger1_R", "r_carpometacarpal_1"),
    ("GameSkeletonThumbFinger2_R", "r_metacarpophalangeal_1"),
    ("GameSkeletonThumbFinger3_R", "r_carpal_interphalangeal_1"),
    
    ("GameSkeletonIndexFinger1_R", "r_carpometacarpal_2"),
    ("GameSkeletonIndexFinger2_R", "r_metacarpophalangeal_2"),
    ("GameSkeletonIndexFinger3_R", "r_carpal_proximal_interphalangeal_2"),
    ("GameSkeletonIndexFinger4_R", "r_carpal_distal_interphalangeal_2"),
    
    ("GameSkeletonMiddleFinger1_R", "r_carpometacarpal_3"),
    ("GameSkeletonMiddleFinger2_R", "r_metacarpophalangeal_3"),
    ("GameSkeletonMiddleFinger3_R", "r_carpal_proximal_interphalangeal_3"),
    ("GameSkeletonMiddleFinger4_R", "r_carpal_distal_interphalangeal_3"),
    
    ("GameSkeletonRingFinger1_R", "r_carpometacarpal_4"),
    ("GameSkeletonRingFinger2_R", "r_metacarpophalangeal_4"),
    ("GameSkeletonRingFinger3_R", "r_carpal_proximal_interphalangeal_4"),
    ("GameSkeletonRingFinger4_R", "r_carpal_distal_interphalangeal_4"),
    
    ("GameSkeletonPinkyFinger1_R", "r_carpometacarpal_5"),
    ("GameSkeletonPinkyFinger2_R", "r_metacarpophalangeal_5"),
    ("GameSkeletonPinkyFinger3_R", "r_carpal_proximal_interphalangeal_5"),
    ("GameSkeletonPinkyFinger4_R", "r_carpal_distal_interphalangeal_5"),
    
    # Hips and Legs - Left
    ("GameSkeletonHip_L", "l_hip"),
    ("GameSkeletonKnee_L", "l_knee"),
    ("GameSkeletonAnkle_L", "l_talocrural"),
    ("GameSkeletonToes_L", "l_metatarsophalangeal_1"),  # General toe joint
    ("GameSkeletonToesEnd_L", "l_tarsal_interphalangeal_1"),
    
    # Hips and Legs - Right
    ("GameSkeletonHip_R", "r_hip"),
    ("GameSkeletonKnee_R", "r_knee"),
    ("GameSkeletonAnkle_R", "r_talocrural"),
    ("GameSkeletonToes_R", "r_metatarsophalangeal_1"),  # General toe joint
    ("GameSkeletonToesEnd_R", "r_tarsal_interphalangeal_1"),
]

print(f"Total mappings: {len(skeleton_map_list)}")
