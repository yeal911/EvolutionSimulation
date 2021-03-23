import time

from EvolutionSimulation.src.Sheep import Sheep
from EvolutionSimulation.src.Wolf import Wolf
from random import choice
import matplotlib.pyplot as plt
import Population
from numpy import *
import numpy as np

sheep = []
wolf = []
x = []
y = []
z = []
for i in range(0, 5):
    sheep.append(Sheep())
    print("Sheep" + str(i) + " is " + str(sheep[i].gene.geneDigits))

for i in range(0, 10):
    wolf.append(Wolf())
    # print("Wolf" + str(i) + " is " + str(wolf[i].gene.geneDigits))

j = 0


# def out_lifespan(population: Population):
#     for i in range(0, len(population)):
#         if population[i].age == population[i].lifespan:
#             population.remove(population[i])
#             i -= 1
#             if i == len(population) - 1:
#                 return
def out_lifespan(population: Population, index: int):
    if population[index].age == population[index].lifespan:
        population.remove(population[index])
        print("Remove ok!！！！")


def population_grow(population: Population):
    i = 0
    while i < len(population):
        population[i].forage()
        result = population[i].grow()
        if not result:
            out_lifespan(population, i)
        i += 1


def population_fight(population: Population, competitor: Population):
    for i in range(0, len(population)):
        randNum = choice([n for n in range(0, len(competitor)) if n != i])
        population[i].attack(competitor[randNum])

        randNum = choice([n for n in range(0, len(competitor)) if n != i])
        population[i].defend(competitor[randNum])


def population_reproduce(population: Population):
    for i in range(0, len(population)):
        randNum = choice([n for n in range(0, len(population)) if n != i])
        new_population = population[i].breed(population[randNum])
        if new_population is not None:
            population.append(new_population)


def population_plot(population: Population, competitor: Population, cycle: int):
    for i in range(0, len(population)):
        x.append(cycle)
        y.append(len(population))
        z.append(len(competitor))
        plt.plot(x, y, 'r')
        plt.plot(x, z, 'b')
        plt.xlabel("day")
        plt.ylabel("number of population")


def evolution(population: Population, competitor: Population, cycle: int):
    population_grow(population)
    population_grow(competitor)

    population_fight(population, competitor)
    population_fight(competitor, population)

    population_reproduce(population)
    population_reproduce(competitor)

    population_plot(population, competitor, cycle)


start = time.time()

while j != 200:
    evolution(sheep, wolf, j)
    j += 1
    end = time.time()
    if end-start > 180:
        break

print(end - start)
# save plot
plt.savefig("./test.jpg")
#
# # show plot
plt.show()
