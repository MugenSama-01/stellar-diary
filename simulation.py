import math
import multiprocessing

_sim_process = None


def _run_ursina_app(logs):
    from ursina import Ursina, Entity, color, window, application
    from ursina.prefabs.first_person_controller import FirstPersonController

    app = Ursina(title="Stellar Diary - 3D Celestial Sphere", borderless=False)

    input_handler = Entity()

    def handle_input(key):
        if key in ('escape', 'q'):
            application.quit()

    input_handler.input = handle_input

    window.color = color.black

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

        scale_val = max(0.4, float(brightness) * 0.5)
        Entity(model='sphere', color=color.white, scale=scale_val, position=(x, y, z), unlit=True)

    app.run()


def make_it_real(logs):
    global _sim_process
    # If a simulation process is currently running, terminate it before starting a fresh one
    if _sim_process is not None and _sim_process.is_alive():
        _sim_process.terminate()
        _sim_process.join(timeout=1)

    _sim_process = multiprocessing.Process(target=_run_ursina_app, args=(logs,), daemon=True)
    _sim_process.start()