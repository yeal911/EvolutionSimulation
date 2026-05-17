# from abc import ABCMeta, abstractmethod
import math
import random
import time

from EvolutionSimulation.src.gene.Gene import Gene
from EvolutionSimulation.src.event.EventLogger import log_event


class Population:
    """this abstract class defines the common actions of population"""

    # defines the population feeding types
    CARNIVORE = 1
    HERBIVORE = 2

    # defines the population types
    ANIMAL = 1
    PLANT = 2

    # Strategy types for reciprocal altruism / prisoner's dilemma
    STRATEGY_ALWAYS_COOP = 0
    STRATEGY_ALWAYS_DEFECT = 1
    STRATEGY_TIT_FOR_TAT = 2
    STRATEGY_RANDOM = 3

    # fight behaviour of a population individual
    def fight(self, competitor):
        # Kin selection: if very similar gene and same species, avoid fighting (altruism toward kin)
        if (competitor.populationType == Population.ANIMAL and
            self.__class__.__name__ == competitor.__class__.__name__):
            similarity = self.gene.similarity(competitor.gene)
            if similarity >= 0.7:
                # Greenbeard effect: if both have same badge, strong altruism
                if self.greenbeardBadge == competitor.greenbeardBadge and self.greenbeardBadge >= 0:
                    log_event("Altruism", f"{self.name} spared {competitor.name} (greenbeard badge {self.greenbeardBadge})")
                    return "Flee"
                # Hamilton's rule approximation: help kin
                if random.random() < similarity * 0.5:
                    log_event("KinSelection", f"{self.name} spared kin {competitor.name} (similarity {similarity:.2f})")
                    return "Flee"

        # if competitor is animal, check if competitor will try to escape
        if competitor.populationType == Population.ANIMAL:
            # Base flee chance: prey always has some chance to escape
            prey_speed = getattr(competitor, 'runningSpeed', 50)
            predator_speed = getattr(self, 'runningSpeed', 50)
            # Faster prey = higher escape chance; base 20% + speed bonus
            base_flee_chance = 0.20 + max(0, (prey_speed - predator_speed)) / 200.0
            if random.random() < base_flee_chance:
                competitor.fleeSuccessTimes += 1
                return "Flee"
            # Original distance-based flee logic (secondary check)
            if self.populationThreat - competitor.populationThreat >= 2:
                distance = math.sqrt(math.pow(self.coordinateX - competitor.coordinateX, 2) + math.pow(self.coordinateY - competitor.coordinateY, 2))
                if self.runningSpeed <= competitor.runningSpeed or distance * 10 / max(1, self.runningSpeed - competitor.runningSpeed) > 10:
                    competitor.fleeSuccessTimes += 1
                    return "Flee"
                else:
                    competitor.fleeFailureTimes += 1
        if self.fightCapability > competitor.fightCapability:
            # win fight, reset properties
            self.hungryLevel = 0
            self.fightTimes += 1
            competitor.ownThread.receiveDefendInfo("Failure", competitor)
            log_event("Fight", f"{self.name} won fight against {competitor.name}")
            return "Success"
        elif self.fightCapability == competitor.fightCapability:
            self.hungryLevel += 1
            competitor.ownThread.receiveDefendInfo("Peace", competitor)
            return "Peace"
        else:
            competitor.ownThread.receiveDefendInfo("Success", competitor)
            self.fightTimes += 1
            self.lifeStatus = "Dead"
            self.deathCause = "Fight to death"
            self.deathTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
            log_event("Fight", f"{self.name} lost fight to {competitor.name}")
            return "Failure"

    # Reciprocal altruism / Prisoner's Dilemma interaction
    def play_pd_game(self, other):
        """Play a prisoner's dilemma mini-game with another animal. Returns (payoff_for_self, my_move, their_move)."""
        my_move = self._pd_move(other)
        their_move = other._pd_move(self)
        # Record moves for Tit-for-Tat
        self.record_pd_opponent_move(other.name, their_move)
        other.record_pd_opponent_move(self.name, my_move)
        # Payoffs: (C,C)=3, (C,D)=0, (D,C)=5, (D,D)=1
        if my_move == "C" and their_move == "C":
            self.reputation += 1
            other.reputation += 1
            return 3, my_move, their_move
        elif my_move == "C" and their_move == "D":
            self.reputation -= 1
            other.reputation += 1
            return 0, my_move, their_move
        elif my_move == "D" and their_move == "C":
            self.reputation += 1
            other.reputation -= 1
            return 5, my_move, their_move
        else:
            return 1, my_move, their_move

    def _pd_move(self, other):
        """Determine cooperate (C) or defect (D) based on strategy gene."""
        strategy = self.pdStrategy
        if strategy == Population.STRATEGY_ALWAYS_COOP:
            return "C"
        elif strategy == Population.STRATEGY_ALWAYS_DEFECT:
            return "D"
        elif strategy == Population.STRATEGY_TIT_FOR_TAT:
            # Cooperate first time, then mirror other's last move
            last = self.pdHistory.get(other.name, None)
            return "C" if last is None or last == "C" else "D"
        else:  # Random
            return "C" if random.random() < 0.5 else "D"

    def record_pd_opponent_move(self, opponent_name, move):
        """Record what opponent did for Tit-for-Tat."""
        self.pdHistory[opponent_name] = move

    # breed behaviour of an animal population individual
    def breed(self, spouse):
        if spouse.__class__.__name__ != self.__class__.__name__ or self.gender == spouse.gender:
            print("Different population or same gender, no breed")
            return None
        # Sexual selection: females evaluate attractiveness
        if self.gender == "F":
            if not self._evaluate_mate(spouse):
                log_event("SexualSelection", f"{self.name} rejected {spouse.name} (attractiveness too low)")
                return None
        elif spouse.gender == "F":
            if not spouse._evaluate_mate(self):
                log_event("SexualSelection", f"{spouse.name} rejected {self.name} (attractiveness too low)")
                return None

        if (self.lowerGrowthPeriod < self.age < self.upperGrowthPeriod) and (spouse.lowerGrowthPeriod < spouse.age < spouse.upperGrowthPeriod):
            # Cooldown: can't breed if bred in the last 1 cycle
            if hasattr(self, '_last_breed_cycle') and self._last_breed_cycle is not None and (self.ownThread.cycleNumber - self._last_breed_cycle) < 1:
                return None
            if hasattr(spouse, '_last_breed_cycle') and spouse._last_breed_cycle is not None and (spouse.ownThread.cycleNumber - spouse._last_breed_cycle) < 1:
                return None
            self.breedTimes += 1
            spouse.breedTimes += 1
            self._last_breed_cycle = self.ownThread.cycleNumber
            spouse._last_breed_cycle = spouse.ownThread.cycleNumber
            self.hungryLevel += 2
            spouse.hungryLevel += 2
            # rebuild gene_set for new baby tiger, get first half gene set from self, another half from spouse
            childGeneDigits = []
            # get first half gene set from self after variation
            parentX = self.gene.variate()
            parentY = spouse.gene.variate()
            for i in range(0, Gene.GENE_LENGTH, 2):
                childGeneDigits.append(parentX.geneDigits[i])
                childGeneDigits.append(parentY.geneDigits[i+1])
            child = self.newChild(Gene(childGeneDigits), math.ceil((self.generation + spouse.generation) / 2 + 1), self.name + "/" + spouse.name)
            log_event("Breed", f"{self.name} + {spouse.name} = {child.name}")
            return child
        return None

    def _evaluate_mate(self, male):
        """Female mate choice - mostly permissive to ensure population sustainability."""
        male_score = male.attractiveness * 0.5 + male.fightCapability * 0.5
        female_standard = self.attractiveness * 0.2 + self.fightCapability * 0.1 + 5
        # Very lenient: most pairs should be accepted
        return male_score >= female_standard * random.uniform(0.3, 1.0)
