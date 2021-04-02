import sys

from EvolutionSimulation.src.Dreamland import Dreamland
from EvolutionSimulation.src.Gene import Gene
import numpy as np
import matplotlib.pyplot as plt

from WolfThread import WolfThread

print(Dreamland.returnSlotCode(99, 54))
print(Dreamland.returnSlotCode(100, 100))
print(Dreamland.returnSlotCode(0, 4))

c = WolfThread(10, Dreamland())

# N = 10
# x = np.random.rand(N)
# y = np.random.rand(N)
# x2 = np.random.rand(N)
# y2 = np.random.rand(N)
# x3 = np.random.rand(N)
# y3 = np.random.rand(N)
# area = np.random.rand(N) * 1000
# fig = plt.figure()
# ax = plt.subplot()
# ax.scatter(x, y, s=area, alpha=0.5)
# ax.scatter(x2, y2, s=area, c='green', alpha=0.6)  # https://blog.csdn.net/qq_36387683/article/details/101378036
# ax.scatter(x3, y3, s=area, c=area, marker='v', cmap='Reds', alpha=0.7)  # 更换标记样式，另一种颜色的样式
# plt.show()

# # 散点图
# n = 1024
# ## 产生随机数
# X = np.random.normal(0, 1, n)
# Y = np.random.normal(0, 1, n)
# ## 产生颜色数
# T = np.arctan2(Y, X)
# plt.figure()
# plt.scatter(X, Y, s=75, c=T, alpha=0.5 )
# plt.xlim((-1.5, 1.5))
# plt.ylim((-1.5, 1.5))
# plt.xticks(())
# plt.yticks(())
# plt.show()














# print(sys.path)
# ge = Gene()
# ge.returnXBitOfGene(2)
# for i in range(0,9):
#     print(i)

# g = Gene()
# # print(g.__class__.__name__)
# from EvolutionSimulation.src.Wolf import Wolf
#
# w1 = Wolf()
# # w1.grow()
# # w1.grow()
# # w1.grow()
# # w1.grow()
# # w1.grow()
# # w1.grow()
# # w1.grow()
# # w1.grow()
# w2 = Wolf()
# # w2.grow()
# # w2.grow()
# # w2.grow()
# # w2.grow()
# # w2.grow()
# # w2.grow()
# # w2.grow()
# # w2.grow()
# w3 = w1.breed(w2)
# w4 = w2.breed(w1)
# print("")