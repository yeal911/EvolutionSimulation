import math
import random


class Dreamland:
    """
    the playground of all populations, with X & Y coordinates.
    The whole dreamland will be divided to different slots per 10 scale.
    The slots are coded with codes like 1010/1020/2010 etc.
    1010 means the rectangle area from [0,0] to (10,10) in the coordinate axis.

    ***parameter explanation***
    populationThreadPlayers: stores all the Population Threads which should be added in Thread's own structure method
    coordinateMap: it is a dict, it has all the land slot no.s as the key, and the value is population individuals which are added/removed from Thread's logic
    """
    SIZE_X = 700
    SIZE_Y = 350

    # Environment types for camouflage (mimicry) simulation
    TERRAIN_PLAIN = 0      # default terrain
    TERRAIN_FOREST = 1     # green/camouflage advantage
    TERRAIN_DESERT = 2     # brown/camouflage advantage
    TERRAIN_WATER = 3      # blue (not usable by animals)
    TERRAIN_MOUNTAIN = 4   # grey

    def __init__(self):
        # all population thread players
        self.populationThreadPlayers = []
        # coordinate map(dict) for searching, key is slot no., value is population individuals.
        self.coordinateMap = {}
        # terrain type for each slot (for camouflage simulation)
        self.terrainMap = {}
        # rich slots: plants regrow faster here (territory simulation)
        self.richSlots = set()
        # nest map: key = slot_code, value = list of Nest objects
        self.nestMap = {}
        # environmental fluctuation cycle (r/K selection simulation)
        self.environmentCycle = 0
        self.environmentHarshness = 0.0  # 0.0 = stable, 1.0 = extreme drought
        self.cycleDuration = 20  # cycles per environmental phase

        # initialize coordinate map and terrain
        for i in range(10, Dreamland.SIZE_X + 1, 10):
            for j in range(10, Dreamland.SIZE_Y + 1, 10):
                mapKey = str(i) + "A" + str(j)
                self.coordinateMap[mapKey] = []
                self.nestMap[mapKey] = []
                # generate terrain based on position (simple clustering)
                self.terrainMap[mapKey] = self._generateTerrain(i, j)

        # randomly designate ~10% of slots as rich
        all_slots = list(self.coordinateMap.keys())
        rich_count = max(1, len(all_slots) // 10)
        self.richSlots = set(random.sample(all_slots, rich_count))

    def _generateTerrain(self, x, y):
        """Generate terrain type based on coordinates with some clustering."""
        # Use coordinate hash to create patches
        patch = (x // 100) * 10 + (y // 100)
        terrain_pool = {
            0: Dreamland.TERRAIN_PLAIN,
            1: Dreamland.TERRAIN_FOREST,
            2: Dreamland.TERRAIN_DESERT,
            3: Dreamland.TERRAIN_WATER,
            4: Dreamland.TERRAIN_MOUNTAIN,
            5: Dreamland.TERRAIN_FOREST,
            6: Dreamland.TERRAIN_DESERT,
            7: Dreamland.TERRAIN_PLAIN,
            8: Dreamland.TERRAIN_MOUNTAIN,
            9: Dreamland.TERRAIN_FOREST,
        }
        # Add some randomness within patch
        if random.random() < 0.15:
            return random.choice(list(terrain_pool.values()))
        return terrain_pool.get(patch, Dreamland.TERRAIN_PLAIN)

    def updateEnvironment(self, cycle_number):
        """Update environmental harshness for r/K selection simulation."""
        self.environmentCycle = cycle_number
        phase = (cycle_number // self.cycleDuration) % 4
        # Phase 0: stable (0.0), Phase 1: mild stress (0.3), Phase 2: harsh (0.7), Phase 3: recovering (0.2)
        harshness_map = {0: 0.0, 1: 0.3, 2: 0.7, 3: 0.2}
        self.environmentHarshness = harshness_map.get(phase, 0.0)
        # Occasionally shift rich slots
        if cycle_number > 0 and cycle_number % self.cycleDuration == 0:
            all_slots = list(self.coordinateMap.keys())
            rich_count = max(1, len(all_slots) // 10)
            self.richSlots = set(random.sample(all_slots, rich_count))

    def isRichSlot(self, slot_code):
        return slot_code in self.richSlots

    def getTerrain(self, slot_code):
        return self.terrainMap.get(slot_code, Dreamland.TERRAIN_PLAIN)

    # # add population player into this dreamland
    # def addPopulationPlayer(self, pt):
    #     self.populationThreadPlayers.append(pt)
    #     pt.start()

    # remove population player from this dreamland
    def removePopulationPlayer(self, pt):
        self.populationThreadPlayers.remove(pt)
        # stop running thread
        pt.join()

    # start population thread
    @staticmethod
    def startPopulationThread(pt):
        pt.start()

    # stop population thread
    @staticmethod
    def stopPopulationThread(pt):
        pt.continueRunning = False

    # return slot code with input x and y coordinates
    @staticmethod
    def returnSlotCode(x, y):
        if x == 0:
            codeX = 10
        else:
            codeX = math.ceil(x/10) * 10
        if y == 0:
            codeY = 10
        else:
            codeY = math.ceil(y/10) * 10
        return str(codeX) + "A" + str(codeY)

    # compute slot code after movement, check whether the target slot still inside the dreamland, if no then return None, otherwise return target slot code
    @staticmethod
    def computeSlot(slot_code, x_slot_shift, y_slot_shift):
        slotNum = slot_code.split("A")
        targetSlotX = int(slotNum[0]) + x_slot_shift * 10
        targetSlotY = int(slotNum[1]) + y_slot_shift * 10
        if targetSlotX > Dreamland.SIZE_X or targetSlotY > Dreamland.SIZE_Y or targetSlotX < 10 or targetSlotY < 10:
            return None
        return str(targetSlotX) + "A" + str(targetSlotY)
