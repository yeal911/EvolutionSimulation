from EvolutionSimulation.src.Sheep import Sheep
from Gene import Gene

sheep1 = Sheep()
sheep2 = Sheep()
# gene = Gene()
# gene1 = Gene()

# print(gene.geneDigits)
# print(gene1.geneDigits)
print("sheep1 gene " + str(sheep1.gene.geneDigits))
print("sheep1 attackPossibility " + str(sheep1.attackPossibility))
print("sheep1 gender " + str(sheep1.gender))

print("sheep2 gene " + str(sheep2.gene.geneDigits))
print("sheep2 defendPossibility " + str(sheep2.defendPossibility))
print("sheep2 gender " + str(sheep2.gender))

sheep3 = Sheep()
gene = sheep1.breed(sheep2)
print(gene, "here")
if gene != None:
    sheep3.set_gene(gene)
    print("s" + str(sheep3.gene.geneDigits))


# gene.recombine(gene1)
# print("returnXBitOfGene " + str(gene.returnXBitOfGene(3)))
# print(gene.geneDigits)
# print(gene.variate().geneDigits)
