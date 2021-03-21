from EvolutionSimulation.src.Sheep import Sheep
import random

sheep = []

for i in range(0, 5):
    sheep.append(Sheep())
    print("Sheep" + str(i) + " is " + str(sheep[i].gene.geneDigits))
j = 0
while j != 200:
    for i in range(0, len(sheep)):
        randomNum = i
        sheep[i].grow()
        sheep[i].forage()
        while randomNum == i:
            randomNum = random.randint(0, len(sheep) - 1)
        sheep[i].attack(sheep[randomNum])
        sheep[i].defend(sheep[randomNum])
        new_sheep = sheep[i].breed(sheep[randomNum])
        if new_sheep is not None:
            sheep.append(new_sheep)
        sheep[i].grow()
        print("len is " + str(len(sheep)) + " i is " + str(i))
    print("j is " + str(j))
    j += 1

# gene = sheep1.breed(sheep2)
# sheep3.set_gene(gene)
# print(gene, "here")
# if gene is not None:
#     print("s " + str(sheep3.gene.geneDigits))


# gene.recombine(gene1)
# print("returnXBitOfGene " + str(gene.returnXBitOfGene(3)))
# print(gene.geneDigits)
# print(gene.variate().geneDigits)
