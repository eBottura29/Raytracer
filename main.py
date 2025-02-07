from pg_extensions import *


class Blocker:
    def __init__(self, position, color):
        self.position = position
        self.color = color

    def is_inside(self, point):
        return False


class CircleBlocker(Blocker):
    def __init__(self, position, color, radius):
        super().__init__(position, color)
        self.radius = radius

    def is_inside(self, point):
        return (point.x - self.position.x) ** 2 + (point.y - self.position.y) ** 2 <= self.radius**2

    def render(self):
        draw_circle(window.SURFACE, self.color, self.position, self.radius)


class RectBlocker(Blocker):
    def __init__(self, position, color, dimentions):
        super().__init__(position, color)
        self.dimentions = dimentions

    def is_inside(self, point):
        return self.position.x <= point.x and point.x < self.position.x + self.dimentions.x and self.position.y <= point.y and point.y < self.position.y + self.dimentions.y

    def render(self):
        draw_rectangle(window.SURFACE, self.color, self.position, self.dimentions)


class Ray:
    def __init__(self, r, theta):
        self.r = r
        self.theta = theta


class Source:
    def __init__(self, position, num_rays, range, resolution):
        self.position = position
        self.num_rays = num_rays
        self.range = range
        self.resolution = resolution

    def compute(self, blockers):
        self.rays = [Ray(self.range, (i / self.num_rays) * 2 * math.pi) for i in range(self.num_rays)]
        self.distances = [self.range for _ in range(self.num_rays)]

        for i, ray in enumerate(self.rays):
            p = self.range / self.resolution
            found = False

            for x in range(self.resolution):
                for blocker in blockers:
                    if blocker.is_inside(Vector2(self.position.x + p * x * math.cos(ray.theta), self.position.y + p * x * math.sin(ray.theta))):
                        self.distances[i] = p * x
                        found = True
                        continue

                if found == True:
                    continue

            if found == True:
                continue

    def render(self, color, radius, ray_color):
        for i, ray in enumerate(self.rays):
            draw_line(
                window.SURFACE,
                ray_color,
                self.position,
                Vector2(self.position.x + self.distances[i] * math.cos(ray.theta), self.position.y + self.distances[i] * math.sin(ray.theta)),
            )

        draw_circle(window.SURFACE, color, self.position, radius)


def start():
    global window, source, blockers, frame
    window = get_window()

    source = Source(Vector2(-200, 0), 500, 750, 200)
    circleBlocker = CircleBlocker(Vector2(300, 100), BLUE, 25)
    rectBlocker = RectBlocker(Vector2(400, 720), BLUE, Vector2(100, 1440))
    blockers = [circleBlocker, rectBlocker]

    frame = 0

    set_window(window)


def update():
    global window, frame
    window = get_window()
    window.SURFACE.fill(BLACK.tup())
    frame += 1

    if input_manager.get_key_down(pygame.K_ESCAPE):
        window.running = False

    source.position.x += 1
    blockers[0].position.y = 300 * math.sin(0.1 * frame)

    source.compute(blockers)

    for blocker in blockers:
        blocker.render()

    source.render(GREEN, 25, WHITE)

    set_window(window)


if __name__ == "__main__":
    run(start, update, 2560, 1440, True, "Raytracer", 999)
