from ir_sim.env import env_base
# from ir_sim.world import 

world_name = 'robot_obstacle_world.yaml'
env = env_base(world_name = world_name, plot=True, init_mode=0, robot_mode='diff')

for i in range(300):

    for robot in env.components['robots'].robot_list:
        des_vel = robot.cal_des_vel()
        robot.move_forward(des_vel)

    env.render()

    









