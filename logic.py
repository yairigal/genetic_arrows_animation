
import random
from itertools import cycle
from math import atan, degrees, pi, cos, sin


class new_draw:
    def __enter__(self):
        pushStyle()

    def __exit__(self, *args, **kw):
        popStyle()


def dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    a = (x1 - x2) * (x1 - x2)
    b = (y1 - y2) * (y1 - y2)
    return (a + b) ** 0.5


class Arrow:
    def __init__(self, x, y, length=100):
        self.r = 50
        self.start_coordinates = [x, y]
        self.reset()
        self.speed = 10
        self.directions = [random.uniform(0 , 2 * pi)
                           for _ in range(length)]

    def _change_direction(self, angle):
        """angle in radians."""
        # self.current_angle += angle
        x = -(self.r * cos(angle))
        y = -(self.r * sin(angle))

        self.end_point[0] = x + self.starting_point[0]
        self.end_point[1] = y + self.starting_point[1]

    def collision_with_walls(self, w, h):
        x, y = self.end_point
        return x < - w / 2 or x > w / 2 or y > h / 2 or y < -h / 2

    def achieved_target(self, x, y):
        return self.end_point == [x, y]

    def is_dead(self, board_size, target):
        w, h = board_size
        x, y = target
        return self.collision_with_walls(w, h) or self.achieved_target(x, y)

    def reset(self):
        x, y = self.start_coordinates
        # initialize the starting and end point
        self.starting_point = [x, y]
        self.end_point = [x, y - self.r]

        # reset the moves generator
        self.moves = self.move_generator()

        # reset fitness
        self.fitness = 0

        # self.current_angle = (pi * 3 / 2) + (pi / 4)

    def angle(self):
        m = self.m()
        if m is None:
            if self.end_point[1] > self.starting_point[1]:
                return pi * 1.5

            else:
                return pi / 2

        elif round(m) == 0:
            if self.end_point[0] > self.starting_point[0]:
                return 0

            else:
                return pi

        a = atan(m)
        # print('m={}, atan={}'.format(m, a))
        return a

    def m(self):
        x0, y0 = self.starting_point
        x1, y1 = self.end_point

        if x1 == x0:
            return None

        return (y1 - y0) / (x1 - x0)

    def _move(self):
        m = self.m()

        if m is None:
            dx = 0
            if self.end_point[1] < self.starting_point[1]:
                dy = -self.speed

            else:
                dy = self.speed

        else:
            dx = (self.speed * self.speed) / ((m * m) + 1)
            dx = dx ** 0.5

            if self.end_point[0] < self.starting_point[0]:
                dx = -dx

            dy = m * dx

        self.starting_point[0] += dx
        self.starting_point[1] += dy

        self.end_point[0] += dx
        self.end_point[1] += dy

    def move_generator(self):
        for direction in cycle(self.directions):
            self._change_direction(direction)
            self._move()
            yield

    def move(self):
        next(self.moves)

    def draw(self):
        x, y = self.starting_point
        x_end, y_end = self.end_point

        # the body
        with new_draw():
            strokeWeight(3)
            line(x, y, x_end, y_end)

        # # lower point
        # with new_draw():
        #     strokeWeight(3)
        #     stroke(255,0,0)
        #     point(*self.starting_point)

        # higher point
        with new_draw():
            strokeWeight(3)
            stroke(0, 0, 255)
            point(*self.end_point)

    def calculate_fitness(self, target):
        max_distance = dist(self.start_coordinates, target)
        dist_to_target = dist(self.end_point, target)
        dist_ratio = max_distance / dist_to_target  # 0 - max_distance

        self.fitness = 2 ** (dist_ratio)


if __name__ == "__main__":
    a = Arrow(0, 0)
    while True:
        a._change_direction(pi/2)
