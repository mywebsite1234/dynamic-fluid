# dynamic-fluid

A small 2D SPH-style (smoothed-particle hydrodynamics) fluid & particle
simulation built on [pygame](https://www.pygame.org/).

## Installation

```bash
pip install dynamic-fluid
```


## Running the demo

The package ships a runnable demo that spawns a pool of water particles and
lets you click-and-drag to blow air at them:

```bash
python -m dynamic_fluid
# or, equivalently
dynamic-fluid
```

Controls:
- **Left click + drag**: spawn air particles that push water around
- **Right click**: erase nearby air particles
- Close the window (or press the window's close button) to quit

## Using it as a library

```python
from dynamic_fluid import*

init()
window = display.set_mode((screen_width, screen_bottom))
optimize_game()

create_particle(fluid_type.Water, 400, 300)

# in your own game loop:
update_physics(all_particles)
update_particles()
draw_particles(window)
display.update()
```

Key public API (see `dynamic_fluid/__main__.py` for a complete usage example):

- `create_particle(fluid_type, x, y)` — spawn a `Water` or `Air` particle
- `update_physics(all_particles)` — advance the SPH physics simulation
- `update_particles()` — run each particle's/air's own per-frame `update()`
- `draw_particles(surface)` — draw all particles onto a pygame surface
- `optimize_game()` — precompute the soft-circle sprite masks used for drawing
- `fluid_type.Water` / `fluid_type.Air` — the available particle types
- `all_particles` / `air_particles` — the live particle lists

## Project layout

```
pyproject.toml
README.md
LICENSE
dynamic_fluid/
    __init__.py      # public API
    __main__.py       # `python -m dynamic_fluid` / `dynamic-fluid` entry point
    CLASS/            # Particle and Air particle classes
    FUNC/             # physics, config, and helper functions
```

## License

MIT, with the [Commons Clause](https://commonsclause.com/) — you're free to
use, modify, and distribute this software (including commercially, e.g.
inside a paid app or game), but you may not sell the software itself (or a
product/service whose value derives substantially from it), and any use
must clearly credit Danylo Stoian as the original author. See
[`LICENSE`](./LICENSE) for the full text.

### License acceptance

The first time you `import dynamic_fluid` (or run `python -m dynamic_fluid` /
`dynamic-fluid`), you'll be asked to type `I AGREE` to accept the license.
Acceptance is remembered afterwards (in `~/.dynamic_fluid/license_accepted`),
so you're only asked once per machine.

In non-interactive contexts (CI, Docker builds, scripts with no attached
terminal), set an environment variable to accept without a prompt:

```bash
export DYNAMIC_FLUID_ACCEPT_LICENSE=1
```
