from EvolutionSimulation.src.Sheep import Sheep
import random
import matplotlib.pyplot as plt
import numpy as np

sheep = []
x = []
y = []

for i in range(0, 5):
    sheep.append(Sheep())
    print("Sheep" + str(i) + " is " + str(sheep[i].gene.geneDigits))

j = 0
while j != 50:
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
        x.append(j)
        y.append(len(sheep))
        # 生成图形
        plt.plot(x, y, 'r')
        plt.xlabel("day")
        plt.ylabel("number of sheep")
        print("len is " + str(len(sheep)) + " i is " + str(i))

    j += 1

# x = np.linspace(-3, 3, 50)
# x = len(sheep)
# y = 2 * x

# # 生成数据
# x = np.arange(0, 10, 0.1) # 横坐标数据为从0到10之间，步长为0.1的等差数组
# y = np.sin(x) # 纵坐标数据为 x 对应的 sin(x) 值


# 显示图形
plt.savefig("./test.jpg")
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
