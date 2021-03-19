from EvolutionSimulation.src.Sheep import Sheep
from Gene import Gene

sheep1 = Sheep()
sheep2 = Sheep()
# gene = Gene()
# gene1 = Gene()

# print(gene.geneDigits)
# print(gene1.geneDigits)

print(sheep1.fightCapability)
print(sheep2.gender)
print(sheep1.gender)
print(sheep1.gene.geneDigits)
print(sheep2.gene.geneDigits)
sheep1.breed(sheep2)

# print(sheep1.attack(sheep2))
# print(sheep1.defend(sheep2))
#
# sheep2.breed(sheep1)
# gene.recombine(gene1)
# print("returnXBitOfGene " + str(gene.returnXBitOfGene(3)))
# print(gene.geneDigits)
# print(gene.variate().geneDigits)
