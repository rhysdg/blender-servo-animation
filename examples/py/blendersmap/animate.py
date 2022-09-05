import sys
import glob
import os
import time 
import itertools
import math
import ujson as json
import functools
from adafruit_servokit import ServoKit
from multiprocessing.pool import ThreadPool,  Pool


class BlenderMap(ServoKit):
    def __init__(self, channels=16, fps=60, cfg= './configs/servo_cfg.json'):
        super(BlenderMap, self).__init__(channels=channels)
        
        self.servo_map = json.load(open(cfg, 'r'))
        self.n_servos = len(self.servo_map)
        self.frame_durationms = 1000/fps
        
    def __setup(self, scene_path):

        limbs = glob.glob(f'{scene_path}/*.json')
        limb_dict = {os.path.splitext(os.path.basename(i))[0]: json.load(open(i, 'r')) for i in limbs}

        return limb_dict
    
    def __set_joint(self,joint, pos):
        if pos == -1:
            self.servo[joint].angle = None
        else:
            self.servo[joint].angle = pos

    def __kill_joints(self):
        for i in range(self.n_servos): 
            self.servo[i].angle = None
        
    def __set_all_joints_mp(self,command_list):
        pool = ThreadPool(len(command_list))
        pool.starmap(self.__set_joint, command_list)
        pool.close()
        pool.join()
        
    def __set_all_joints(self, command_list):
        for joint, pos in command_list:
            self.__set_joint(joint,  pos) 

    def servo_control(self, frame_count=0, frames=3000, scene_path = '/home/rhysdg/blender-servo-animation/examples/py/wake_wave'):

        self.__kill_joints()
        limb_dict = self.__setup(scene_path)

        assert len(limb_dict) > 0, 'incorrect scene folder location! check your path and run again.' 

        animation_durationsms = frames * self.frame_durationms

        start = time.time() *1000

        while True:
            current_time = time.time() *1000
            position_time = current_time - start
            
            if (position_time >= animation_durationsms):
                start_time = current_time
            else:
                frame = math.floor(position_time / self.frame_durationms)
                command_list = [(self.servo_map[i], int(limb_dict[i]['positions']['Bone'][frame])) for i in limb_dict]
            
                
                self.__set_all_joints(command_list)
                        
                if frame >= (frames-1):
                    self.__kill_joints()
                    break
        

if __name__ == "__main__":
    

    bm = BlenderMap(cfg='./configs/servo_cfg.json')
    bm.servo_control(scene_path = '/home/rhysdg/blender-servo-animation/examples/py/wake_wave',
                    frames=1500)
