
from logic import Arrow
from math import pi
import random

w, h = 700, 700


global counter, direction, population, direction_amount
counter = 1
generation = 0

# genetic alg parameters
population_size = 1000
direction_amount = 30
mutation_rate = 0.01
selection_percentage = 0.1

starting_poing = 0, 0
target = 0, -h / 2 + 20


def setup():
    global population
    size(w, h)

    frameRate(30)

    population = [Arrow(0, 0, direction_amount) for _ in range(population_size)]



def is_generation_over():
    global population

    finished = all(arrow.is_dead((w, h), target) for arrow in population)

    return finished


def crossover(father, mother):
    global population, direction_amount

    son = Arrow(0, 0, direction_amount)
    son.directions = father.directions[:direction_amount / 2] + mother.directions[direction_amount / 2:]
    return son

def draw():
    global counter, direction_amount, population_size, selection_percentage, generation, population
    background(255)
    translate(w / 2, h / 2)

    # draw point
    strokeWeight(5)
    stroke(0, 255, 0)
    point(*target)

    counter += 1
    # fitness test
    for arrow in population:
        if not arrow.is_dead((w, h), target):
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
            arrow.calculate_fitness(target)
        
        print('selecting')

        # selection
        population = sorted(population, key=lambda item: item.fitness, reverse=True)
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
                    arrrow.directions[i] = random.uniform(0, 2* pi)

        # reset arrows
        for arrow in population:
            arrow.reset()


            

# changes :
#   lower angle movments
#   set less moves and higher speed (maybe add acceleration?)
#   
