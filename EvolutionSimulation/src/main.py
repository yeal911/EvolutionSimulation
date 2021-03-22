from EvolutionSimulation.src.Sheep import Sheep
import random
from random import choice
import matplotlib.pyplot as plt
import Population
import numpy as np

sheep = []
wolf = []
x = []
y = []

for i in range(0, 5):
    sheep.append(Sheep())
    print("Sheep" + str(i) + " is " + str(sheep[i].gene.geneDigits))

j = 0


# while j != 100:
#     for i in range(0, len(sheep)):
#         randomNum = i
#         sheep[i].grow()
#         sheep[i].forage()
#         while randomNum == i:
#             randomNum = random.randint(0, len(sheep) - 1)
#         sheep[i].attack(sheep[randomNum])
#         sheep[i].defend(sheep[randomNum])
#         new_sheep = sheep[i].breed(sheep[randomNum])
#         if new_sheep is not None:
#             sheep.append(new_sheep)
#         sheep[i].grow()
#         x.append(j)
#         y.append(len(sheep))
#         # generate plot
#         plt.plot(x, y, 'r')
#         plt.xlabel("day")
#         plt.ylabel("number of sheep")
#         print("len is " + str(len(sheep)) + " i is " + str(i))
#
#     j += 1

def evolution(population: Population, competitor: Population, cycle: int):
    for i in range(0, len(population)):
        randNum = choice([n for n in range(0, len(population)) if n != i])
        population[i].grow()
        population[i].forage()
        population[i].attack(competitor[randNum])

        randNum = choice([n for n in range(0, len(population)) if n != i])
        population[i].defend(competitor[randNum])

        randNum = choice([n for n in range(0, len(population)) if n != i])
        new_population = population[i].breed(population[randNum])
        if new_population is not None:
            population.append(new_population)
        x.append(cycle)
        y.append(len(population))
        # generate plot
        plt.plot(x, y, 'r')
        plt.xlabel("day")
        plt.ylabel("number of sheep")


while j != 80:
    evolution(sheep, sheep, j)
    j += 1

# save plot
plt.savefig("./test.jpg")

# show plot
plt.show()
# gene = sheep1.breed(sheep2)
# sheep3.set_gene(gene)
# print(gene, "here")
# if gene is not None:
#     print("s " + str(sheep3.gene.geneDigits))


# gene.recombine(gene1)
# print("returnXBitOfGene " + str(gene.returnXBitOfGene(3)))
# print(gene.geneDigits)
# print(gene.variate().geneDigits)
