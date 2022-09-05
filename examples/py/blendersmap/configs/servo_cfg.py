import json 

servo_map = {'head-lr': 0,  'head-ud': 1,  'pelvis-top':3,  
                        'pelvis-bottom': 2, 'base':4,  'shoulder-ud-l': 5, 
                        'shoulder-lr-l': 6,  'wrist-ud-l': 7,  'wrist-rot-l':  8, 
                        'shoulder-ud-r': 9,  'shoulder-lr-r': 10,  'wrist-ud-r': 11,  
                        'wrist-rot-r': 12}


with open('servo_cfg.json', 'w') as f:
    json.dump(servo_map, f)