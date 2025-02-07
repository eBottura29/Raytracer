from pg_extensions import *


def start():
    pass


def update():
    global window
    window = get_window()

    if input_manager.get_key_down(pygame.K_ESCAPE):
        window.running = False

    set_window(window)


if __name__ == "__main__":
    run(start, update, 2560, 1440, True, "Raytracer", 999)
