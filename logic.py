
import random
from itertools import cycle
from math import atan, degrees, pi, cos, sin

from common import new_draw, w, h


def dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    a = (x1 - x2) * (x1 - x2)
    b = (y1 - y2) * (y1 - y2)
    return (a + b) ** 0.5


# from google
def line_intersection(line1, line2):
    (p0x, p0y), (p1x, p1y) = line1
    (p2x, p2y), (p3x, p3y) = line2

    s1x = p1x - p0x
    s1y = p1y - p0y
    s2x = p3x - p2x
    s2y = p3y - p2y
    s = (-s1y * (p0x - p2x) + s1x * (p0y - p2y)) / (-s2x * s1y + s1x * s2y)
    t = (s2x * (p0y - p2y) - s2y * (p0x - p2x)) / (-s2x * s1y + s1x * s2y)
    return s >= 0 and s <= 1 and t >= 0 and t <= 1


class Arrow:
    def __init__(self, x, y, obstacles, target, length=100):
        self.r = 50
        self.start_coordinates = [x, y]
        self.obstacles = obstacles
        self.target = target
        self.reset()
        self.speed = 2
        self.directions = [random.uniform(-pi/4, pi/4)
                           for _ in range(length)]

    def _change_direction(self, angle):
        """angle in radians."""
        self.current_angle += angle

    def collision_with_walls(self):
        x, y = self.end_point
        return x < - w / 2 or x > w / 2 or y > h / 2 or y < -h / 2

    def achieved_target(self):
        return line_intersection([self.starting_point, self.end_point], self.target)

    def collision_with_obstacles(self):
        for obs in self.obstacles:
            x1, y1, x2, y2 = obs
            if line_intersection([self.starting_point, self.end_point], [(x1, y1), (x2, y2)]):
                return True

        return False

    def is_dead(self):
        return self.collision_with_walls() or self.achieved_target() or self.collision_with_obstacles()

    def reset(self):
        # initialize the starting and end point
        self.starting_point = self.start_coordinates[:]

        # reset the moves generator
        self.moves = self.move_generator()

        # reset fitness
        self.fitness = 0

        self.current_angle = (pi * 3 / 2) + (pi / 4)

    @property
    def end_point(self):
        x, y = self.starting_point
        return x + self.r * cos(self.current_angle), y + self.r * sin(self.current_angle)

    def _move(self):
        x0, y0 = self.starting_point
        self.starting_point = [x0 + self.speed * cos(self.current_angle),
                               y0 + self.speed * sin(self.current_angle)]

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
            if self.is_dead():
                stroke(0, 0, 255)

            if self.achieved_target():
                stroke(0, 255, 0)

            line(x, y, x_end, y_end)

        # # lower point
        # with new_draw():
        #     strokeWeight(3)
        #     stroke(255,0,0)
        #     point(*self.starting_point)

        # higher point
        with new_draw():
            strokeWeight(3)
            stroke(255, 255, 0)
            point(*self.end_point)

    def calculate_fitness(self):
        (x0, y0), (x1, y1) = self.target
        mid_point = (x0 + x1) / 2, (y0 + y1) / 2  # middle point in target
        max_distance = dist(self.start_coordinates, mid_point)
        dist_to_target = dist(self.end_point, mid_point)
        dist_ratio = max_distance / dist_to_target  # 0 - max_distance

        self.fitness = 2 ** (dist_ratio)

        # check for collision with obstacles
        if self.collision_with_obstacles():
            self.fitness = self.fitness ** 0.05
            return

        # if achieved point get a bonus
        if self.achieved_target():
            self.fitness = self.fitness ** 3


if __name__ == "__main__":
    # a = Arrow(0, 0)
    # while True:
    #     a._change_direction(pi/2)
    line1 = [(0, 5), (5, 0)]
    line2 = [(0, 0), (5, 5)]
    print(line_intersection(line1, line2))
