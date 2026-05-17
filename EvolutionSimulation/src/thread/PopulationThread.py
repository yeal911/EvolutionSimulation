import inspect
import random
import time

from EvolutionSimulation.src.dreamland.Dreamland import Dreamland
from EvolutionSimulation.src.population.Plant import Plant
from EvolutionSimulation.src.population.Population import Population
from EvolutionSimulation.src.tool.CycleInfo import CycleInfo
from EvolutionSimulation.src.event.EventLogger import log_event
from EvolutionSimulation.src.nest.Nest import Nest
from EvolutionSimulation.src.parasite.Parasite import Parasite


class PopulationThread:
    """this abstract class defines the common actions of population thread"""

    # # return individual count of a population in the Thread
    # @abstractmethod
    # def getIndividualCount(self): pass

    # update coordinate map after individual's location changing
    def updateDreamLandMap(self, individual: Population, original_slot_code, target_slot_code):
        if original_slot_code is not None:
            self.removeIndividualFromMap(original_slot_code, individual)
        self.appendIndividual2Map(target_slot_code, individual)

    # move individual location
    def moveLocation(self, individual: Population):
        # possible slots to move to
        targetSlotForSearching = [[1, 0], [2, 0], [0, -1], [0, -2], [-1, 0], [-2, 0], [0, 1], [0, 2]]
        # check if the current slot is near the border of dreamland, remove slots beyond dreamland
        slotNum = individual.slotCode.split("A")
        slotX = int(slotNum[0])
        slotY = int(slotNum[1])
        tmpXGap = int(2 - (Dreamland.SIZE_X - slotX) / 10)
        tmpYGap = int(2 - (Dreamland.SIZE_Y - slotY) / 10)
        while 0 < tmpXGap <= 2:
            targetSlotForSearching.remove([tmpXGap, 0])
            tmpXGap -= 1
        while 0 < tmpYGap <= 2:
            targetSlotForSearching.remove([0, tmpYGap])
            tmpYGap -= 1
        tmpXGap = int(slotX / 10)
        tmpYGap = int(slotY / 10)
        while 0 <= tmpXGap < 2:
            targetSlotForSearching.remove([tmpXGap - 2, 0])
            tmpXGap += 1
        while 0 <= tmpYGap < 2:
            targetSlotForSearching.remove([0, tmpYGap - 2])
            tmpYGap += 1
        # move location randomly
        randDirection = random.randint(0, len(targetSlotForSearching) - 1)
        targetShift = targetSlotForSearching[randDirection]
        targetSlot = Dreamland.computeSlot(individual.slotCode, targetShift[0], targetShift[1])
        if targetSlot is not None:
            individual.coordinateX += targetShift[0] * 10
            individual.coordinateY += targetShift[1] * 10
            self.updateDreamLandMap(individual, individual.slotCode, targetSlot)

    # search food in near 2 slots from 4 directions
    def searchFood(self, individual: Population):
        # near areas to be searched, refer to searching logic
        targetSlotForSearching = [[0, 0], [1, 1], [1, 0], [2, 0], [1, -1], [0, -1], [0, -2], [-1, -1], [-1, 0], [-2, 0], [-1, 1], [0, 1], [0, 2]]
        for targetShift in targetSlotForSearching:
            targetSlot = Dreamland.computeSlot(individual.slotCode, targetShift[0], targetShift[1])
            if targetSlot is not None:
                targetSlotIndividuals = self.dreamland.coordinateMap[targetSlot]
                for food in targetSlotIndividuals:
                    if food.lifeStatus == "Alive":
                        if (individual.populationFeedingType == Population.CARNIVORE and food.populationType == Population.ANIMAL and individual.populationName != food.populationName) or (individual.populationFeedingType == Population.HERBIVORE and food.populationType == Population.PLANT):
                            # check target's threat (e.g. wolf won't attach tiger)
                            if individual.populationThreat >= food.populationThreat:
                                # Camouflage check: if prey camouflage matches terrain, predator may miss it
                                if food.populationType == Population.ANIMAL:
                                    terrain = self.dreamland.getTerrain(targetSlot)
                                    # Simple camouflage logic: higher camouflage = harder to detect
                                    if hasattr(food, 'camouflage'):
                                        detect_chance = 1.0 - (food.camouflage / 150.0)
                                        if random.random() > detect_chance:
                                            continue  # missed due to camouflage
                                return food
        return None

    # search spouse in near 2 slots from 4 directions
    def searchSpouse(self, individual: Population):
        # near areas to be searched, refer to searching logic
        targetSlotForSearching = [[0, 0], [1, 1], [1, 0], [2, 0], [1, -1], [0, -1], [0, -2], [-1, -1], [-1, 0], [-2, 0], [-1, 1], [0, 1], [0, 2]]
        candidates = []
        for targetShift in targetSlotForSearching:
            targetSlot = Dreamland.computeSlot(individual.slotCode, targetShift[0], targetShift[1])
            if targetSlot is not None:
                targetSlotIndividuals = self.dreamland.coordinateMap[targetSlot]
                for spouse in targetSlotIndividuals:
                    if spouse.lifeStatus == "Alive":
                        if spouse.populationType == Population.ANIMAL and individual.populationName == spouse.populationName and individual.gender != spouse.gender:
                            candidates.append(spouse)
        # Sexual selection: if female, pick the most attractive male
        if individual.gender == "F" and candidates:
            # Evaluate candidates and pick best
            best = None
            best_score = -1
            for c in candidates:
                score = getattr(c, 'attractiveness', 50) * 0.6 + c.fightCapability * 0.4
                if score > best_score:
                    best_score = score
                    best = c
            return best
        elif candidates:
            return random.choice(candidates)
        return None

    # remove an individual from coordinate map
    def removeIndividualFromMap(self, slotCode, individualForRemove: Population):
        self.dreamland.coordinateMap[slotCode].remove(individualForRemove)

    # append an individual to coordinate map
    def appendIndividual2Map(self, slotCode, individualForAppend: Population):
        self.dreamland.coordinateMap[slotCode].append(individualForAppend)
        individualForAppend.slotCode = slotCode

    # receive cycle info for defending
    def receiveDefendInfo(self, fight_result, pop: Population):
        ownCycles = self.recorder.cycleInfo[self.THREAD_NAME]
        while ownCycles.get(self.cycleNumber, None) is None:
            time.sleep(0.01)
        cycle = ownCycles[self.cycleNumber]
        cycle.defendTimes += 1
        pop.fightTimes += 1
        if fight_result == "Success":
            pop.hungryLevel = 0
            cycle.defendSuccessTimes += 1
        elif fight_result == "Failure":
            pop.lifeStatus = "Dead"
            pop.deathCause = "Fight to death"
            pop.deathTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
            cycle.defendFailureTimes += 1
        else:
            pop.hungryLevel += 1
            cycle.defendPeaceTimes += 1

    # add individual to thread
    def addIndividual2Thread(self, pop: Population):
        pop.coordinateX = random.randint(0, Dreamland.SIZE_X)
        pop.coordinateY = random.randint(0, Dreamland.SIZE_Y)
        pop.slotCode = Dreamland.returnSlotCode(pop.coordinateX, pop.coordinateY)
        pop.ownThread = self
        self.group.append(pop)
        self.updateDreamLandMap(pop, None, pop.slotCode)

    def _try_build_nest(self, individual, cycleInfo):
        """Extended phenotype: build a nest if tendency is high enough."""
        if getattr(individual, 'territoryTendency', 0) > 60 and individual.hungryLevel < 5:
            slot = individual.slotCode
            if len(self.dreamland.nestMap.get(slot, [])) < 3:
                quality = min(5, max(1, individual.territoryTendency // 20))
                nest = Nest(individual.name, slot, individual.coordinateX, individual.coordinateY, quality)
                self.dreamland.nestMap[slot].append(nest)
                individual.ownedNest = nest
                individual.hungryLevel += 1
                cycleInfo.nestBuilt += 1
                log_event("Nest", f"{individual.name} built nest at {slot} (quality {quality})")

    def _handle_nest_bonus(self, individual, cycleInfo):
        """Apply nest breeding bonus if individual owns a nest here."""
        if individual.ownedNest and individual.ownedNest.slotCode == individual.slotCode:
            if individual.hungryLevel > 0:
                individual.hungryLevel = max(0, individual.hungryLevel - individual.ownedNest.get_breeding_bonus())
            cycleInfo.nestUsed += 1

    def _handle_parasites(self, individual, cycleInfo):
        """Parasite infection and clearing."""
        # Chance to get infected
        if random.random() < 0.05 and not individual.parasites:
            parasite = Parasite(individual.name, individual.slotCode)
            individual.parasites.append(parasite)
            cycleInfo.parasiteAttachments += 1
            log_event("Parasite", f"{individual.name} infected by parasite (virulence {parasite.virulence})")
        # Existing parasites drain and may be cleared
        for p in list(individual.parasites):
            if p.active:
                p.drain(individual)
                if p.try_clear(individual.gene.geneDigits[3]):
                    cycleInfo.parasiteCleared += 1
            if not p.active:
                individual.parasites.remove(p)

    def _territory_defense(self, individual, cycleInfo):
        """Territorial behavior: defend rich slots."""
        if getattr(individual, 'territoryTendency', 0) > 40 and self.dreamland.isRichSlot(individual.slotCode):
            # Check for intruders in the same slot
            intruders = [i for i in self.dreamland.coordinateMap.get(individual.slotCode, [])
                         if i != individual and i.lifeStatus == "Alive"
                         and i.populationType == Population.ANIMAL
                         and i.__class__.__name__ == individual.__class__.__name__]
            for intruder in intruders:
                if random.random() < individual.territoryTendency / 200.0:
                    cycleInfo.territoryDefenses += 1
                    log_event("Territory", f"{individual.name} defends territory against {intruder.name}")
                    # Drive intruder away
                    self.moveLocation(intruder)
                    intruder.hungryLevel += 1

    def _pd_interaction(self, individual, cycleInfo):
        """Prisoner's Dilemma interaction with a nearby conspecific."""
        if getattr(individual, 'pdStrategy', Population.STRATEGY_ALWAYS_DEFECT) == Population.STRATEGY_ALWAYS_DEFECT:
            return
        nearby = self.dreamland.coordinateMap.get(individual.slotCode, [])
        partners = [p for p in nearby if p != individual and p.lifeStatus == "Alive"
                    and p.populationType == Population.ANIMAL
                    and p.__class__.__name__ == individual.__class__.__name__]
        if partners and random.random() < 0.3:
            partner = random.choice(partners)
            payoff, my_move, their_move = individual.play_pd_game(partner)
            # Convert payoff to hunger effect
            if payoff >= 3:
                individual.hungryLevel = max(0, individual.hungryLevel - 1)
                cycleInfo.pdCooperateTimes += 1
            elif payoff == 5:
                individual.hungryLevel = max(0, individual.hungryLevel - 2)
                cycleInfo.pdDefectTimes += 1
            log_event("PD", f"{individual.name}({my_move}) vs {partner.name}({their_move}) payoff={payoff}")

    # monitor all individuals, and execute for all their actions, any thread has different logic, just overwrite this method
    def animalThreadRun(self):
        while self.continueRunning:
            self.num.append(len(self.group))
            print(self.THREAD_NAME + " cycle: " + str(self.cycleNumber + 1) + ".  Remaining individual: " + str(len(self.group)))
            cycleInfo = CycleInfo(self.THREAD_NAME)
            # Update environment for r/K selection simulation
            self.dreamland.updateEnvironment(self.cycleNumber)
            if len(self.group) != 0:
                self.cycleNumber += 1
                for individual in self.group:
                    # Parasite handling
                    if hasattr(individual, 'parasites'):
                        self._handle_parasites(individual, cycleInfo)

                    # check if individual should die naturally
                    if individual.hungryLevel > 10:
                        individual.lifeStatus = "Dead"
                        individual.deathCause = "Starve to death"
                        cycleInfo.newDeathFromStarve += 1
                    elif individual.age >= individual.lifespan:
                        individual.lifeStatus = "Dead"
                        individual.deathCause = "Natural death"
                        cycleInfo.newDeathFromNatural += 1
                    elif individual.deathCause == "Fight to death":
                        cycleInfo.newDeathFromFight += 1
                    # check individual life status first, move to different category if dead
                    if individual.lifeStatus == "Dead":
                        individual.deathTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
                        self.group.remove(individual)
                        self.dead.append(individual)
                        cycleInfo.newDeath += 1
                        # Clean up nest
                        if hasattr(individual, 'ownedNest') and individual.ownedNest:
                            slot = individual.ownedNest.slotCode
                            if individual.ownedNest in self.dreamland.nestMap.get(slot, []):
                                self.dreamland.nestMap[slot].remove(individual.ownedNest)
                        continue
                    if not individual.isBusy:
                        individual.isBusy = True

                        # Extended phenotype: nest building
                        if hasattr(individual, 'territoryTendency'):
                            self._try_build_nest(individual, cycleInfo)

                        # Territory defense
                        if hasattr(individual, 'territoryTendency'):
                            self._territory_defense(individual, cycleInfo)

                        # Prisoner's Dilemma interaction
                        if hasattr(individual, 'pdStrategy'):
                            self._pd_interaction(individual, cycleInfo)

                        # add logic for searching food and fight
                        if individual.hungryLevel > 5:
                            # find food in its own slot, if there is, then fight, if none, change position
                            food = self.searchFood(individual)
                            if food is not None and not food.isBusy:
                                cycleInfo.fightTimes += 1
                                fightResult = individual.fight(food)
                                # if wins, update location to food's location, and remove food from map
                                if fightResult == "Success":
                                    individual.coordinateX = food.coordinateX
                                    individual.coordinateY = food.coordinateY
                                    self.updateDreamLandMap(individual, individual.slotCode, food.slotCode)
                                    self.removeIndividualFromMap(food.slotCode, food)
                                    cycleInfo.fightSuccessTimes += 1
                                    individual.moveHistory[self.cycleNumber] = str(individual.coordinateX) + "|" + str(individual.coordinateY) + "," + individual.slotCode
                                # if fails, remove individual from map
                                elif fightResult == "Failure":
                                    self.removeIndividualFromMap(individual.slotCode, individual)
                                    cycleInfo.fightFailureTimes += 1
                                elif fightResult == "Flee":
                                    cycleInfo.FleeSuccessTimes += 1
                            # if no food found, move location and become more hungry
                            else:
                                self.moveLocation(individual)
                                individual.hungryLevel += 1
                                individual.moveHistory[self.cycleNumber] = str(individual.coordinateX) + "|" + str(individual.coordinateY) + "," + individual.slotCode
                        # if not hungry enough, prepare for breeding
                        else:
                            individual.hungryLevel += 1
                            # Nest bonus before breeding
                            self._handle_nest_bonus(individual, cycleInfo)
                            # breed logic
                            spouse = self.searchSpouse(individual)
                            if spouse is not None and not spouse.isBusy:
                                cycleInfo.breedTimes += 1
                                child = individual.breed(spouse)
                                if child is not None:
                                    self.addIndividual2Thread(child)
                                    cycleInfo.newBorn += 1
                                else:
                                    cycleInfo.sexualRejections += 1
                    individual.isBusy = False
                    individual.age += 1
                    cycleInfo.popAvgHungryLevel += individual.hungryLevel
                    cycleInfo.popAvgAge += individual.age
                    cycleInfo.popAvgLifespan += individual.lifespan
                    cycleInfo.popAvgFightCapability += individual.fightCapability
                    cycleInfo.popAvgAttackPossibility += individual.attackPossibility
                    cycleInfo.popAvgDefendPossibility += individual.defendPossibility
                    cycleInfo.popAvgTotalBreedingTimes += individual.totalBreedingTimes
                    if hasattr(individual, 'camouflage'):
                        cycleInfo.popAvgCamouflage += individual.camouflage
                    if hasattr(individual, 'attractiveness'):
                        cycleInfo.popAvgAttractiveness += individual.attractiveness
                    if hasattr(individual, 'territoryTendency'):
                        cycleInfo.popAvgTerritoryTendency += individual.territoryTendency
                # if there is still live population
                cycleInfo.liveIndividuals = len(self.group)
                cycleInfo.deadIndividuals = len(self.dead)
                if len(self.group) != 0:
                    cycleInfo.popAvgHungryLevel = round(cycleInfo.popAvgHungryLevel / len(self.group), 2)
                    cycleInfo.popAvgAge = round(cycleInfo.popAvgAge / len(self.group), 2)
                    cycleInfo.popAvgLifespan = round(cycleInfo.popAvgLifespan / len(self.group), 2)
                    cycleInfo.popAvgFightCapability = round(cycleInfo.popAvgFightCapability / len(self.group), 2)
                    cycleInfo.popAvgAttackPossibility = round(cycleInfo.popAvgAttackPossibility / len(self.group), 2)
                    cycleInfo.popAvgDefendPossibility = round(cycleInfo.popAvgDefendPossibility / len(self.group), 2)
                    cycleInfo.popAvgTotalBreedingTimes = round(cycleInfo.popAvgTotalBreedingTimes / len(self.group), 2)
                    cycleInfo.popAvgCamouflage = round(cycleInfo.popAvgCamouflage / len(self.group), 2)
                    cycleInfo.popAvgAttractiveness = round(cycleInfo.popAvgAttractiveness / len(self.group), 2)
                    cycleInfo.popAvgTerritoryTendency = round(cycleInfo.popAvgTerritoryTendency / len(self.group), 2)
                self.recorder.saveCycleInfo(self.cycleNumber, self, cycleInfo)
                # sleep for 1 day (1s)
                time.sleep(1)
            # if all individuals are dead
            else:
                break
            self.newBronNum.append(cycleInfo.newBorn)
            self.newDeathNum.append(cycleInfo.newDeath)
            self.avgHungryLevel.append(cycleInfo.popAvgHungryLevel)
            self.avgLifespan.append(cycleInfo.popAvgLifespan)
            self.avgFightCapability.append(cycleInfo.popAvgFightCapability)
            self.avgAge.append(cycleInfo.popAvgAge)
            self.avgAttackPossibility.append(cycleInfo.popAvgAttackPossibility)
            self.avgDefendPossibility.append(cycleInfo.popAvgDefendPossibility)
            self.avgTotalBreedingTimes.append(cycleInfo.popAvgTotalBreedingTimes)
            self.avgCamouflage.append(cycleInfo.popAvgCamouflage)
            self.avgAttractiveness.append(cycleInfo.popAvgAttractiveness)
            self.avgTerritoryTendency.append(cycleInfo.popAvgTerritoryTendency)

    # plant thread run
    def plantThreadRun(self):
        while self.continueRunning:
            self.num.append(len(self.group))
            print(self.THREAD_NAME + " cycle: " + str(self.cycleNumber + 1) + ".  Remaining individual: " + str(len(self.group)))
            self.cycleNumber += 1
            cycleInfo = CycleInfo(self.THREAD_NAME)
            # Environment affects plant growth (r/K selection)
            base_limit = int(Dreamland.SIZE_X * Dreamland.SIZE_Y) / 100
            harshness = self.dreamland.environmentHarshness
            adjusted_limit = int(base_limit * (1.0 - harshness * 0.6))
            # generate new plants in each round if plants count is less than adjusted limit
            if len(self.group) < adjusted_limit:
                # Rich slots produce more plants
                actual_count = self.cyclePlantCount
                if harshness > 0.5:
                    actual_count = max(1, self.cyclePlantCount // 2)
                for i in range(0, actual_count):
                    plant = Plant()
                    self.addIndividual2Thread(plant)
                cycleInfo.newBorn = actual_count
            if len(self.group) != 0:
                for individual in self.group:
                    # check if individual should die naturally
                    if individual.age >= individual.lifespan:
                        individual.lifeStatus = "Dead"
                        individual.deathCause = "Natural death"
                        cycleInfo.newDeathFromNatural += 1
                    elif individual.deathCause == "Fight to death":
                        cycleInfo.newDeathFromFight += 1
                    # check individual life status first, move to different category if dead
                    if individual.lifeStatus == "Dead":
                        individual.deathTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
                        self.group.remove(individual)
                        self.dead.append(individual)
                        cycleInfo.newDeath += 1
                        continue
                    individual.age += 1
                    cycleInfo.popAvgAge += individual.age
                    cycleInfo.popAvgLifespan += individual.lifespan
                    cycleInfo.popAvgFightCapability += individual.fightCapability
                    cycleInfo.popAvgAttackPossibility += individual.attackPossibility
                    cycleInfo.popAvgDefendPossibility += individual.defendPossibility
            # if there is still live population
            cycleInfo.liveIndividuals = len(self.group)
            cycleInfo.deadIndividuals = len(self.dead)
            if len(self.group) != 0:
                cycleInfo.popAvgAge = round(cycleInfo.popAvgAge / len(self.group), 2)
                cycleInfo.popAvgLifespan = round(cycleInfo.popAvgLifespan / len(self.group), 2)
                cycleInfo.popAvgFightCapability = round(cycleInfo.popAvgFightCapability / len(self.group), 2)
                cycleInfo.popAvgAttackPossibility = round(cycleInfo.popAvgAttackPossibility / len(self.group), 2)
                cycleInfo.popAvgDefendPossibility = round(cycleInfo.popAvgDefendPossibility / len(self.group), 2)
            self.recorder.saveCycleInfo(self.cycleNumber, self, cycleInfo)
            # sleep for 1 day (1s)
            time.sleep(1)
            self.newDeathNum.append(cycleInfo.newDeath)
