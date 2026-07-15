"""dynamic_fluid: a small 2D SPH-style fluid & particle simulation built on pygame.

Import the package and drive your own simulation with functions like
``create_particle()``, ``update_physics()`` and ``draw_particles()`` (see
``dynamic_fluid.__main__`` for a full usage example), or just run the
bundled demo with ``python -m dynamic_fluid`` / the ``dynamic-fluid``
command.
"""

from ._license_gate import ensure_license_accepted

ensure_license_accepted()

from .coda2 import *  # noqa: F401,F403,E402
from .CLASS.Air_CLASS import Air  # noqa: F401
from .FUNC import fluid_type, fluid  # noqa: F401
from .FUNC.config import (  # noqa: F401
    all_particles,
    air_particles,
    screen_width,
    screen_bottom,
    circle_radius,
    circle_diameter,
    pool_height,
    pool_spacing,
)

__version__ = "0.1.0"
