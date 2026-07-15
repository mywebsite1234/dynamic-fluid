from .. import coda as var

class Particle:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.vel_x = 0
        self.vel_y = 0
        self.density = 0
        self.pressure = 0
        self.force_x = 0
        self.force_y = 0
        # self.is_flying = False
    def update(self):
        var.particle_choords[id(self)] = self
        # if self.is_flying:
        #     # print("test")
        #     self.vel_y -= 50