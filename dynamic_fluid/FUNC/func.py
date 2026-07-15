from .cappo import*
from ..coda0 import*


def measure_distance(particle_a, particle_b):
    dx = particle_a.x - particle_b.x
    dy = particle_a.y - particle_b.y
    return sqrt(dx * dx + dy * dy)

def calculate_direction(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    angle_radians = atan2(dy, dx)
    angle_degrees = degrees(angle_radians)
    
    final_angle = (angle_degrees + 360) % 360
    return final_angle

def create_grid(all_particles):
    grid = {}
    cell_size = radar_range 
    
    for particle in all_particles:
        grid_x = int(particle.x // cell_size)
        grid_y = int(particle.y // cell_size)
        
        particle.grid_x = grid_x
        particle.grid_y = grid_y
        
        if (grid_x, grid_y) not in grid:
            grid[(grid_x, grid_y)] = []
        grid[(grid_x, grid_y)].append(particle)
        
    return grid

def get_neighbors(particle, grid):
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            cell = (particle.grid_x + dx, particle.grid_y + dy)
            if cell in grid:
                neighbors.extend(grid[cell])
    return neighbors

def refresh_neighbor_lists(all_particles, grid):
    for particle in all_particles:
        particle.neighbors = get_neighbors(particle, grid)

def calculate_density_and_pressure(all_particles):
    max_allowed_pressure = 50.0  
    radar_sq = radar_range * radar_range
    
    for particle_a in all_particles:
        particle_a.density = radar_range 
        particle_a.neighbor_data = []
        
        for particle_b in particle_a.neighbors:
            if particle_a is not particle_b:
                dx = particle_a.x - particle_b.x
                dy = particle_a.y - particle_b.y
                dist_sq = dx * dx + dy * dy

                if dist_sq < radar_sq:
                    if dist_sq == 0:
                        distance = 0.001
                        dx, dy = 0.001, 0.001
                    else:
                        distance = sqrt(dist_sq)

                    kernel_score = radar_range - distance
                    particle_a.density += kernel_score
                    particle_a.neighbor_data.append((particle_b, dx, dy, distance, kernel_score))

            # for air in air_particles:
            #     if sqrt((air.x - particle_b.x)**2 + (air.y - particle_b.y)**2) <= 20:
            #         if fluid.aircollide(particle_b, air):
            #             particle_b.is_flying = True

        raw_pressure = stiffness * (particle_a.density - rest_density)
        particle_a.pressure = min(max_allowed_pressure, max(-0.2, raw_pressure))

def apply_air_buoyancy(particle):
    influence_sq = air_influence_range * air_influence_range

    for air in air_particles:
        dx = particle.x - air.x
        dy = particle.y - air.y
        dist_sq = dx * dx + dy * dy

        if dist_sq < influence_sq and dist_sq > 0:
            distance = sqrt(dist_sq)
            lift = buoyancy_strength * (1.0 - distance / air_influence_range)
            particle.force_y -= lift

def calculate_forces(all_particles):
    for particle_a in all_particles:
        particle_a.force_x = 0
        particle_a.force_y = gravity
        apply_air_buoyancy(particle_a)
        
        for particle_b, dx, dy, distance, kernel in particle_a.neighbor_data:
            dir_x = dx / distance
            dir_y = dy / distance

            push_strength = (particle_a.pressure + particle_b.pressure) * kernel

            particle_a.force_x += dir_x * push_strength
            particle_a.force_y += dir_y * push_strength

            speed_diff_x = particle_b.vel_x - particle_a.vel_x
            speed_diff_y = particle_b.vel_y - particle_a.vel_y
            viscosity_weight = kernel / radar_range

            particle_a.force_x += speed_diff_x * viscosity_strength * viscosity_weight
            particle_a.force_y += speed_diff_y * viscosity_strength * viscosity_weight

def update_positions(all_particles, dt, extra_damping=1.0):
    drag = (100 - air_ressistance) / 100
    margin = circle_radius

    for particle in all_particles:
        particle.vel_x = (particle.vel_x + particle.force_x * dt) * drag * velocity_damping * extra_damping
        particle.vel_y = (particle.vel_y + particle.force_y * dt) * drag * velocity_damping * extra_damping

        speed = sqrt(particle.vel_x**2 + particle.vel_y**2)

        if speed > max_speed:
            particle.vel_x = (particle.vel_x / speed) * max_speed
            particle.vel_y = (particle.vel_y / speed) * max_speed

        particle.x += particle.vel_x * dt
        particle.y += particle.vel_y * dt

        if particle.y >= screen_bottom - margin:
            particle.y = screen_bottom - margin - uniform(0.0, 0.35)
            if particle.vel_y > 0:
                particle.vel_y *= -floor_bounce
            particle.vel_x *= floor_friction

        if particle.y <= margin:
            particle.y = margin + uniform(0.0, 0.35)
            if particle.vel_y < 0:
                particle.vel_y *= -wall_bounce

        if particle.x <= margin:
            particle.x = margin + uniform(0.0, 0.35)
            if particle.vel_x < 0:
                particle.vel_x *= -wall_bounce
            particle.vel_y *= wall_friction

        if particle.x >= screen_width - margin:
            particle.x = screen_width - margin - uniform(0.0, 0.35)
            if particle.vel_x > 0:
                particle.vel_x *= -wall_bounce
            particle.vel_y *= wall_friction

_physics_frame_count = 0

def update_physics(all_particles):
    global _physics_frame_count
    _physics_frame_count += 1

    extra_damping = settle_in_damping if _physics_frame_count <= settle_in_frames else 1.0

    substep = time_step / physics_iterations

    for _ in range(physics_iterations):
        grid = create_grid(all_particles)
        refresh_neighbor_lists(all_particles, grid)
        calculate_density_and_pressure(all_particles)
        calculate_forces(all_particles)
        update_positions(all_particles, substep, extra_damping)

def optimize_game():
    global circle_surface, game_is_optimized, air_surface
    game_is_optimized = True
    
    circle_surface = Surface((circle_diameter, circle_diameter), SRCALPHA)
    
    for i in range(circle_radius, 0, -1):
        alpha = int(255 * (1.0 - (i / circle_radius)))
        draw.circle(circle_surface, (255, 255, 255, alpha), (circle_radius, circle_radius), i)

    air_surface = Surface((circle_diameter, circle_diameter), SRCALPHA)
    draw.circle(air_surface, (255, 0, 0), (circle_radius, circle_radius), circle_radius)

def create_particle(input_fluid_type: fluid_type.Fluid | None = None, x: int | None = None, y: int | None = None):
    """create (spawn) a new particle.
    
    Args:
        input_fluid_type (fluid_type): the fluid to spawn (using the format "fluid_type.Desired_Fluid_Name") NOTE: not all fluids are avalible
        x (int): the x location the fluid is spawned at.
        y (int): the y location the fluid is spawned at.
    """
    if input_fluid_type == fluid_type.Water:
        new_drop = Particle(x, y)
        all_particles.append(new_drop)
    elif input_fluid_type == fluid_type.Air:
        if len(air_particles) != 0:
            old_molecule = air_particles[-1]
            old_molecule.other_particle_direction = calculate_direction(old_molecule.x, old_molecule.y, x, y)
        new_molecule = Air(x, y)
        air_particles.append(new_molecule)

def draw_particles(draw_surface: Surface):
    window = draw_surface
    if game_is_optimized:
        fluid_canvas = Surface((screen_width, screen_bottom), SRCALPHA)

        for particle in all_particles:
            fluid_canvas.blit(circle_surface, ((int(particle.x) - circle_radius), (int(particle.y) - circle_radius)))
        
        fluid_mask = mask.from_surface(fluid_canvas, threshold=100)
        mask_surface = fluid_mask.to_surface(setcolor=(50, 150, 255, 255), unsetcolor=(0, 0, 0, 0))
        window.blit(mask_surface, (0, 0))

        for particle in air_particles:
            window.blit(air_surface, ((int(particle.x) - circle_radius), (int(particle.y) - circle_radius)))
            
    elif not game_is_optimized:
        for particle in all_particles:
            draw.circle(window, (50, 150, 255), (int(particle.x), int(particle.y)), circle_radius)
        for particle in air_particles:
            draw.circle(window, (255, 0, 0), (int(particle.x), int(particle.y)), circle_radius)

def update_particles():
    for particle in all_particles:
        particle.update()
    for air in air_particles:
        air.update()