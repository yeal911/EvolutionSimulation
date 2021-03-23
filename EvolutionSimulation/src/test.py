import sys
from EvolutionSimulation.src.Gene import Gene

# print(sys.path)
# ge = Gene()
# ge.returnXBitOfGene(2)
# for i in range(0,9):
#     print(i)

# g = Gene()
# print(g.__class__.__name__)
from EvolutionSimulation.src.Wolf import Wolf

w1 = Wolf()
# w1.grow()
# w1.grow()
# w1.grow()
# w1.grow()
# w1.grow()
# w1.grow()
# w1.grow()
# w1.grow()
w2 = Wolf()
# w2.grow()
# w2.grow()
# w2.grow()
# w2.grow()
# w2.grow()
# w2.grow()
# w2.grow()
# w2.grow()
w3 = w1.breed(w2)
w4 = w2.breed(w1)
print("")