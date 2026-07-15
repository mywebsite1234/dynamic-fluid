"""Runnable demo app for dynamic_fluid.

Launch it with:

    python -m dynamic_fluid

or, after installing the package, with the console script:

    dynamic-fluid
"""

from . import (
    init,
    quit,
    display,
    event,
    mouse,
    time,
    QUIT,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    uniform,
    fluid_type,
    all_particles,
    air_particles,
    screen_width,
    screen_bottom,
    circle_radius,
    pool_height,
    pool_spacing,
    optimize_game,
    create_particle,
    update_particles,
    update_physics,
    draw_particles,
)


def main():
    init()
    black = (0, 0, 0)
    is_pressed = False
    particle_x = -1
    particle_y = -1
    new_particle_x = particle_x
    new_particle_y = particle_y
    particle_start_is_init = False

    optimize_game()

    size_window = (screen_width, screen_bottom)
    window = display.set_mode(size_window)
    display.set_caption('Game')

    for x_pos in range(circle_radius, screen_width - circle_radius, pool_spacing):
        for y_pos in range(screen_bottom - pool_height, screen_bottom - circle_radius, pool_spacing):
            drop_x = uniform(-0.5, 0.5)
            drop_y = uniform(-0.5, 0.5)

            create_particle(fluid_type.Water, x_pos + drop_x, y_pos + drop_y)

    run = True
    while run:
        for e in event.get():
            if e.type == QUIT:
                run = False
            if e.type == MOUSEBUTTONDOWN:
                is_pressed = True
            if e.type == MOUSEBUTTONUP:
                is_pressed = False

        window.fill(black)
        update_physics(all_particles)

        if is_pressed:
            pos = mouse.get_pos()
            pressed = mouse.get_pressed()
            new_particle_x = pos[0]
            new_particle_y = pos[1]
            if not particle_start_is_init and pressed[0]:
                particle_start_is_init = True
                particle_x = pos[0]
                particle_y = pos[1]
                create_particle(fluid_type.Air, new_particle_x, new_particle_y)
            elif pressed[2]:
                for air in air_particles[:]:
                    if ((pos[0] - air.x) ** 2 + (pos[1] - air.y) ** 2) ** 0.5 <= circle_radius + 2:
                        air_particles.remove(air)
            else:
                if new_particle_x != particle_x and new_particle_y != particle_y and pressed[0]:
                    create_particle(fluid_type.Air, new_particle_x, new_particle_y)
                    particle_x = new_particle_x
                    particle_y = new_particle_y

        update_particles()
        draw_particles(window)

        display.update()
        time.delay(16)

    quit()


if __name__ == "__main__":
    main()
