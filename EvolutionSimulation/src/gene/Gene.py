#!/usr/bin/python3
import random


class Gene:
    # 基因序列
    seq = []
    # 基因序列长度
    gene_length = 10
    # 变异幅度
    __variate_bits = 1
    # 基因适应度
    gene_fitness_grade = 0

    def __init__(self, input_seq):
        self.seq = []  # 很奇怪这个地方要置空, 第二次new对象的时候会引用到之前的list里面的东西
        if input_seq == "" or input_seq is None:
            self.seq = Gene.create_gene_random(self.gene_length)
        else:
            for index in range(1, len(input_seq)+1):
                self.seq.append(str(input_seq[index - 1:index]))
                # self.seq = seq

    # 获取基因长度
    @staticmethod
    def get_gene_length(self):
        return 10

    # 基因变异
    def variate(self):
        variated_index = []
        for index in range(0, self.__variate_bits):
            random_index = random.randint(0, self.gene_length-1)
            while random_index in variated_index:
                random_index = random.randint(0, self.gene_length-1)
            else:
                variated_index.append(random_index)
            if self.seq[random_index] == "0":
                self.seq[random_index] = "1"
            else:
                self.seq[random_index] = "0"

    # 输出基因序列
    def output(self):
        tmp_str = ""
        for tmp in self.seq:
            tmp_str += str(tmp)
        return tmp_str + ": " + str(self.gene_fitness_grade)

    # 输出基因序列
    def print_gene(self):
        tmp_str = ""
        for tmp in self.seq:
            tmp_str += str(tmp)
        print(tmp_str + ": " + str(self.gene_fitness_grade))

    # 随机创建基因序列
    @staticmethod
    def create_gene_random(count):
        init_str = []
        for index in range(count):
            init_str.append(str(random.randint(0, 1)))
        return init_str

    # 基因繁殖
    @staticmethod
    def gene_multiply(father, mother):
        multiply_gene_str = ""
        for index in range(0, father.gene_length):
            if index < father.gene_length/2:
                multiply_gene_str = multiply_gene_str + father.seq[index]
            else:
                multiply_gene_str = multiply_gene_str + mother.seq[index]
        return Gene(multiply_gene_str)
#
# g = gene(None)
# g.print_gene()
#
# g.variate()
# g.print_gene()

