from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import math

import backend


def make_it_alive(logs):
    print(logs)
    app = Ursina()

    window.color = color.black

    def input(key):
        if key == 'escape':
            application.quit()

    player = FirstPersonController()
    player.speed = 0
    player.jump_height = 0
    player.gravity = 0
    player.rotation_x = 0

    ground = Entity(
        model='plane',
        scale=(200, 1, 200),
        texture='grass',
        texture_scale=(100, 100),
        color=color.gray,
        position=(0, -2, 0),
    )

    sphere_radius = 200

    for az, alt, brightness in logs:
        az_rad = math.radians(az)
        alt_rad = math.radians(alt)

        x = sphere_radius * math.cos(alt_rad) * math.sin(az_rad)
        y = sphere_radius * math.sin(alt_rad)
        z = sphere_radius * math.cos(alt_rad) * math.cos(az_rad)

        Entity(model='sphere', color=color.white, scale=brightness * 0.5, position=(x, y, z), unlit=True)

    app.run()