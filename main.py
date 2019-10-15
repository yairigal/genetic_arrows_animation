
from logic import Arrow
from math import pi
import random
from common import w, h, new_draw


counter = 1
generation = 0

# genetic alg parameters
population_size = 1000
direction_amount = 70
mutation_rate = 0.05
selection_percentage = 0.01

starting_poing = 0, 200
target = [(-30, -h / 2 + 20), (30, -h / 2 + 20)]
obstacles = [(-w/2, 100, 50, 100),
             (-50, -50, w/2, -50),
             (-w/2, -200, 50, -200)]


def setup():
    global population
    size(w, h)
    frameRate(60)

    population = [Arrow(*starting_poing, obstacles=obstacles, target=target, length=direction_amount)
                  for _ in range(population_size)]


def is_generation_over():
    global population

    finished = all(arrow.is_dead() for arrow in population)

    return finished


def crossover(father, mother):
    global population, direction_amount

    son = Arrow(*starting_poing, obstacles=obstacles,
                target=target, length=direction_amount)
    son.directions = father.directions[:direction_amount /
                                       2] + mother.directions[direction_amount / 2:]
    return son



a = Arrow(0,0,[],[(10,10),(20,20)])
def draw():
    global counter
    counter += 1
    background(255)
    translate(w / 2, h / 2)
    if counter % 30 == 0:
        a._change_direction(pi/4)
    a._move()
    a.draw()


def draw1():
    global obstacles, counter, direction_amount, population_size, selection_percentage, generation, population
    background(255)
    translate(w / 2, h / 2)

    # draw point
    with new_draw():
        strokeWeight(10)
        stroke(255, 0, 0)
        (a, b), (c, d) = target
        line(a, b, c, d)

    # draw obstacle
    for obs in obstacles:
        with new_draw():
            strokeWeight(10)
            stroke(0)
            line(*obs)

    counter += 1
    # fitness test
    for arrow in population:
        if not arrow.is_dead():
            arrow.move()

        arrow.draw()

    if counter >= direction_amount or is_generation_over():
        generation += 1
        print('generation #{} is over'.format(generation))
        # generation is over
        counter = 0

        print('calculating fitness')
        # calcualte fitness
        for arrow in population:
            arrow.calculate_fitness()

        print('selecting')

        # selection
        population = sorted(
            population, key=lambda item: item.fitness, reverse=True)
        population = population[:int(population_size * selection_percentage)]

        print('Crossover')

        # crossover
        new_pop = population[:]  # copy the population NOT by referance
        for _ in range(population_size - len(population)):
            father = random.choice(population)
            mother = random.choice(population)
            descendent = crossover(father, mother)
            new_pop.append(descendent)

        del population
        population = new_pop

        print('mutation')

        # mutation
        for arrrow in population:
            for i in range(direction_amount):
                if random.random() <= mutation_rate:
                    arrrow.directions[i] = random.uniform(-pi/4, pi/4)

        # reset arrows
        for arrow in population:
            arrow.reset()


# changes :
#   lower angle movments
#   set less moves and higher speed (maybe add acceleration?)
#
