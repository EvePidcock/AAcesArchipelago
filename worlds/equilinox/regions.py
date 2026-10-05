from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region
from rule_builder.rules import Has

if TYPE_CHECKING:
    from .world import EquilinoxWorld

def create_and_connect_regions(world: EquilinoxWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: EquilinoxWorld) -> None:
    menu = Region("Menu", world.player, world.multiworld)

    regions = [menu]

    world.multiworld.regions += regions


def connect_regions(world: EquilinoxWorld) -> None:
    return
