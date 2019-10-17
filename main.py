
from logic import Arrow
from math import pi
import random
from common import w, h, new_draw

counter = 1
generation = 0

# genetic alg parameters
population_size = 500
direction_amount = 500
mutation_rate = 0.5
selection_percentage = 0.05

starting_poing = 0, 400
target = [(-30, -h / 2 + 20), (30, -h / 2 + 20)]
# hard map
# obstacles = [(100, 250, 100, 0),
#              (100, 0, -100, 0),
#              (-100, 0, -100, 250),
#              (-100, 0, -100, -100),
#              (-100, -100, -w/2, -100),
#              (50, -100, 150, -100),
#              (150, -100, 150, -50),
#              (150, -50, w/2,-50)]

#multiple way map
obstacles = [(150, 0, -150, 0),
             (-w/2, -100, -100, -100),
             (100, -100, w/2, -100),
             (-150, -200, 150, -200)]


def generate_obstacale(y,r_length=150):
    x = random.uniform(-w/2, w/2 - r_length)
    return x, y, x + r_length, y


def generate_terrain():
    amount_in_row = 10
    start_y = -250

    lines = []
    for i in range(6):
        a = [generate_obstacale(start_y + 100*i, 40) for _ in range(amount_in_row)]
        lines.extend(a)
    return lines


def crossover(father, mother):
    global population, direction_amount

    son = Arrow(*starting_poing, obstacles=obstacles,
                target=target, length=direction_amount)

    new_directions = [(dir1 + dir2)/2 for dir1,
                      dir2 in zip(father.directions, mother.directions)]
    son.directions = new_directions
    return son



def genetic_algorithm():
    global mutation_rate, obstacles, counter, direction_amount, population_size, selection_percentage, generation, population
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
    new_pop = []
    for _ in range(population_size - len(population)):
        father = random.choice(population)
        mother = random.choice(population)
        descendent = crossover(father, mother)
        new_pop.append(descendent)


    print('mutation')

    # mutation
    for arrrow in new_pop:
        for i in range(direction_amount):
            if random.random() <= mutation_rate:
                arrrow.directions[i] = random.uniform(-pi/4, pi/4)
    
    population = new_pop + population
    del new_pop

    # reset arrows
    for arrow in population:
        arrow.reset()


def setup():
    global population, obstacles
    size(w, h)
    frameRate(1000)
    # obstacles = generate_terrain()
    population = [Arrow(*starting_poing, obstacles=obstacles, target=target, length=direction_amount)
                  for _ in range(population_size)]


def draw():
    global mutation_rate, obstacles, counter, direction_amount, population_size, selection_percentage, generation, population
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

    print('fitness test')
    # fitness test
    for arrow in population:
        if not arrow.is_dead():
            arrow.move()

        arrow.draw()

    if counter >= direction_amount or all(arrow.is_dead() for arrow in population):
        generation += 1
        print('generation #{} is over'.format(generation))
        # generation is over
        counter = 0

        genetic_algorithm()
        
    
    


# changes :
# randomize terrain with boxes.
# make fitness function work with number of steps