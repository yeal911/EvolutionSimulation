#!/usr/bin/python3
import random
import copy
import typing


class Gene:
    """this class defines the properties and behaviours of generic gene"""

    # gene length
    GENE_LENGTH = 10

    # gene bit min value
    __geneBitMinValue = 0

    # gene bit max value
    __geneBitMaxValue = 99

    # gene variation min digits
    __geneVariationMinValue = 0

    # gene variation max digits
    __geneVariationMaxValue = 2

    # initialize a new gene
    def __init__(self, gene_digits=None):
        # gene digits
        self.geneDigits = []
        if gene_digits is None:
            i = 0
            while i < Gene.GENE_LENGTH:
                self.geneDigits.append(random.randint(Gene.__geneBitMinValue, Gene.__geneBitMaxValue))
                i += 1
        else:
            self.geneDigits = gene_digits

    # # return specific bit of a gene
    # def returnXBitOfGene(self, x):
    #     if x > Gene.__geneLength or x < 0 or not isinstance(x, int):
    #         print("returnXBitOfGene: X out of gene bit range!")
    #         return None
    #     else:
    #         return self.geneDigits[x - 1]

    # Gene variation, return a new Gene object
    def variate(self):
        variationCopy = copy.deepcopy(self)
        variationDigitCount = random.randint(Gene.__geneVariationMinValue, Gene.__geneVariationMaxValue)
        # print("variationDigitCount " + str(variationDigitCount))
        exclude = []
        while variationDigitCount > 0:
            variationBit = random.choice([i for i in range(0, 9) if i not in exclude])
            # print("variationBit " + str(variationBit))
            exclude.append(variationBit)
            variationCopy.geneDigits[variationBit] = random.randint(Gene.__geneBitMinValue, Gene.__geneBitMaxValue)
            variationDigitCount -= 1
        return variationCopy

    def recombine(self, spouse):
        recombineGene = Gene()
        for i in range(0, Gene.GENE_LENGTH):
            randomNum = random.randint(0, 1)
            if randomNum == 0:
                recombineGene.geneDigits.append(self.geneDigits[i])
            else:
                recombineGene.geneDigits.append(spouse.geneDigits[i])
        randomNum = random.randint(0, 9)
        if randomNum == 9:
            recombineGene = recombineGene.variate()
            print("Random number is " + str(randomNum) + " gene variates")
        print("Gene recombination result is " + str(recombineGene.geneDigits))
        return recombineGene

    # return the summary of all digits in the gene
    def sumGeneDigits(self):
        summaryValue = 0
        for i in range(0, Gene.GENE_LENGTH):
            summaryValue += self.geneDigits[i]
        return summaryValue