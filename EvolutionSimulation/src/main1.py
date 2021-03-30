import time

from EvolutionSimulation.src.Sheep import Sheep
from EvolutionSimulation.src.Wolf import Wolf
from random import choice, random
import matplotlib.pyplot as plt
import Population
from numpy import *
import numpy as np

sheep = []
wolf = []

x = []
y = []
z = []
for i in range(0, 15):
    sheep.append(Sheep())
    print("Sheep" + str(i) + " is " + str(sheep[i].gene.geneDigits))

for i in range(0, 15):
    wolf.append(Wolf())

j = 0


def out_lifespan(population: Population, index: int):
    if population[index].lifeStatus == "Dead":
        print("Remove ok!！！！" + population[index].name)
        population.remove(population[index])


def population_grow(population: Population):
    i = 0
    while i < len(population):
        population[i].forage()
        result = population[i].grow()
        if not result:
            out_lifespan(population, i)
        i += 1


def population_fight(population: Population, competitor: Population):
    for i in range(0, round(len(population) * 0.2)):
        randNum = random.randint(0, len(competitor) - 1)
        # randNum = choice([n for n in range(0, len(competitor)) if n != i])
        population[i].fight(competitor[randNum])
        # competitor[randNum].fight(population[i])


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
    # population_forage(population, competitor)
    # population_forage(competitor, population)

    population_fight(population, competitor)

    population_reproduce(population)
    population_reproduce(competitor)

    population_plot(population, competitor, cycle)


start = time.time()

while j != 100:
    # print("j is " + str(j))
    # print("sheep " + str(len(sheep)))
    # print("wolf " + str(len(wolf)))
    evolution(sheep, wolf, j)

    j += 1
    end = time.time()
    if end - start > 280:
        break

print(end - start)
# save plot
plt.savefig("./test.jpg")
#
# # show plot
plt.show()
