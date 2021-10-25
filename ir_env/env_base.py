import yaml
import numpy as np
from ir_world import env_plot, mobile_robot, car_robot
from ir_env.env_robot import env_robot
from PIL import Image
import sys

class env_base:

    def __init__(self, world_name=None, plot=True, **kwargs):

        if world_name != None:
            world_name = sys.path[0] + '/' + world_name
            
            with open(world_name) as file:
                com_list = yaml.load(file, Loader=yaml.FullLoader)

                world_args = com_list['world']
                self.__height = world_args.get('world_height', 10)
                self.__width = world_args.get('world_width', 10)
                self.__step_time = world_args.get('step_time', 0.1)
                self.world_map =  world_args.get('world_map', None)
                self.xy_reso = world_args.get('xy_resolution', 1)
                self.yaw_reso = world_args.get('yaw_resolution', 5)

                self.robots_args = com_list.get('robots', None)

                if self.robots_args != None:
                    self.robot_number = self.robots_args.get('number', 0)
                else:
                    self.robot_number = 0

                cars = com_list.get('cars', None)

                if cars != None:
                    self.car_number = cars.get('number', 0)
                else:
                    self.car_number = 0      
        else:
            self.__height = kwargs.get('world_height', 10)
            self.__width = kwargs.get('world_width', 10)
            self.__step_time = kwargs.get('step_time', 0.1)
            self.world_map = kwargs.get('world_map', None)
            self.xy_reso = kwargs.get('xy_resolution', 1)
            self.yaw_reso = kwargs.get('yaw_resolution', 5)
                    
        self.plot = plot
        self.components = dict()
        self.init_environment(**kwargs)

    def init_environment(self, robot_class=mobile_robot, car_class=car_robot, **kwargs):

        # world
        px = int(self.__width / self.xy_reso)
        py = int(self.__height / self.xy_reso)

        if self.world_map != None:
            
            world_map_path = sys.path[0] + '/' + self.world_map
            img = Image.open(world_map_path).convert('L')
            img = img.resize( (px, py), Image.NEAREST)
            map_matrix = np.array(img)
            map_matrix = 255 - map_matrix
            map_matrix[map_matrix>255/2] = 255
            map_matrix[map_matrix<255/2] = 0
            self.map_matrix = np.fliplr(map_matrix.T)
        else:
            self.map_matrix = np.zeros([px, py])

        self.components['map_matrix'] = self.map_matrix

        if self.robot_number != 0:
            temp = {**self.robots_args, **kwargs}
            robots = env_robot(robot_class=robot_class, step_time=self.__step_time, **temp)
            self.components['robots'] = robots
        else:
            self.components['robots'] = None

        if self.plot:
            self.world_plot = env_plot(self.__width, self.__height, self.components, **kwargs)
    
    def render(self, time=0.05, **kwargs):
        self.world_plot.com_cla()
        self.world_plot.draw_dya_components(**kwargs)
        self.world_plot.pause(time)
        
    def show(self):
        self.world_plot.show()
    
    def show_ani(self):
        self.world_plot.show_ani()
    
    def save_ani(self):
        self.world_plot.save_ani()

    



        
        
            
    
        

        

