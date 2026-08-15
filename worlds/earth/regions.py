from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region
from rule_builder.rules import Has

if TYPE_CHECKING:
    from .world import EarthWorld

def create_and_connect_regions(world: EarthWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: EarthWorld) -> None:
    main = Region("Main", world.player, world.multiworld)
    events = Region("Events", world.player, world.multiworld)

    regions = [main, events]

    world.multiworld.regions += regions


def connect_regions(world: EarthWorld) -> None:
    main = world.get_region("Main")
    events = world.get_region("Events")

    main.connect(events, "Main to Events", Has("Event Cards"))

