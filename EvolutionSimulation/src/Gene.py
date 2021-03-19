#!/usr/bin/python3
import random
import copy
import typing

class Gene:
    """this class defines the properties and behaviours of generic gene"""

    # gene length
    __geneLength = 10

    # gene bit min value
    __geneBitMinValue = 0

    # gene bit max value
    __geneBitMaxValue = 9

    # gene variation min digits
    __geneVariationMinValue = 0

    # gene variation max digits
    __geneVariationMaxValue = 5

    # initialize a new gene
    def __init__(self, gene=None):
        # gene digits
        self.geneDigits = []
        if gene == None:
            i = 0
            while i < Gene.__geneLength:
                self.geneDigits.append(random.randint(Gene.__geneBitMinValue, Gene.__geneBitMaxValue))
                i += 1




    # return specific bit of a gene
    def returnXBitOfGene(self, x):
        if x > Gene.__geneLength or x < 0 or not isinstance(x, int):
            print("returnXBitOfGene: X out of gene bit range!")
            return None
        else:
            return self.geneDigits[x - 1]

    # Gene variation, return a new Gene object
    def variate(self):
        variationCopy = copy.deepcopy(self)
        variationDigitCount = random.randint(Gene.__geneVariationMinValue, Gene.__geneVariationMaxValue)
        print("variationDigitCount " + str(variationDigitCount))
        exclude = []
        while variationDigitCount > 0:
            variationBit = random.choice([i for i in range(0, 9) if i not in exclude])
            print("variationBit " + str(variationBit))
            exclude.append(variationBit)
            variationCopy.geneDigits[variationBit] = random.randint(Gene.__geneBitMinValue, Gene.__geneBitMaxValue)
            variationDigitCount -= 1
        print("variationCopy " + str(len(variationCopy.geneDigits)))
        return variationCopy

    def recombine(self, spouse):
        recombineGene = Gene()
        for i in range(0, Gene.__geneLength):
            randomNum = random.randint(0, 1)
            if randomNum == 0:
                recombineGene.geneDigits.append(self.geneDigits[i])
            else:
                recombineGene.geneDigits.append(spouse.geneDigits[i])
        print("Gene recombination result is " + str(recombineGene.geneDigits))
        return recombineGene



