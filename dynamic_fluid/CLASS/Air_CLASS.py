from .. import coda as var
from math import*
# from FUNC.fluid import aircollide

class Air:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.other_particle_direction = -1
        self.chnk_size = 10
    def update(self):
        neighbors = []
        for pid, water_particle in var.particle_choords.items():
            x_value = water_particle.x
            y_value = water_particle.y
            if abs(self.x - x_value) <= self.chnk_size and abs(self.y - y_value) <= self.chnk_size and sqrt((self.x - x_value)**2 + (self.y - y_value)**2) <= var.circle_radius*2+3:
                neighbors.append(pid)
                water_speed = sqrt(water_particle.vel_x**2 + water_particle.vel_y**2)
                angle_radians = radians(self.other_particle_direction)
                new_x_vel = water_speed * cos(angle_radians)
                new_y_vel = water_speed * sin(angle_radians)
                water_particle.vel_x = new_x_vel * 10
                water_particle.vel_y = new_y_vel * 10
