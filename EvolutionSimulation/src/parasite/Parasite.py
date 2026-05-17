import random
import time

from EvolutionSimulation.src.dreamland.Dreamland import Dreamland
from EvolutionSimulation.src.event.EventLogger import log_event


class Parasite:
    """Parasite that attaches to animals and drains their resources."""

    def __init__(self, host_name, host_slot, virulence=None):
        self.hostName = host_name
        self.slotCode = host_slot
        self.virulence = virulence if virulence is not None else random.randint(1, 5)
        self.attachTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.active = True

    def drain(self, host):
        """Drain host's hunger level each cycle."""
        if not self.active:
            return 0
        drain_amount = self.virulence
        host.hungryLevel += drain_amount
        return drain_amount

    def try_clear(self, host_immune_gene):
        """Chance to be cleared based on host immune strength."""
        # immune strength approximated by gene digit (using gene[3] as proxy for immune)
        immune = host_immune_gene / 99.0
        if random.random() < immune * 0.3:
            self.active = False
            log_event("Parasite", f"{self.hostName} cleared parasite (immune {host_immune_gene})")
            return True
        return False
