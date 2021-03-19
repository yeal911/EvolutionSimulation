from EvolutionSimulation.src.Sheep import Sheep
from Gene import Gene
from numpy import *

# sheep1 = Sheep(5, 6)
# sheep2 = Sheep(7, 8)
gene = Gene()
gene1 = Gene()


print(gene.geneDigits)

print(sheep1.fightCapability)
print(sheep2.gender)
print(sheep1.gender)

print(sheep1.attack(sheep2))
print(sheep1.defend(sheep2))

print("returnXBitOfGene " + str(gene.returnXBitOfGene(3)))
print(gene.geneDigits)
print(gene.variate().geneDigits)
