import time


class Nest:
    """Represents a nest built by an animal (extended phenotype)."""

    def __init__(self, builder_name, slot_code, coordinate_x, coordinate_y, quality=1):
        self.builderName = builder_name
        self.slotCode = slot_code
        self.coordinateX = coordinate_x
        self.coordinateY = coordinate_y
        self.quality = quality  # 1-5, affects breeding bonus
        self.buildTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.usageCount = 0
        self.active = True

    def use(self):
        """Called when an animal uses this nest for breeding."""
        self.usageCount += 1

    def get_breeding_bonus(self):
        """Return hunger recovery bonus from using the nest."""
        return self.quality * 2

    def get_defense_bonus(self):
        """Return defense bonus for the owner inside the nest."""
        return self.quality * 5
