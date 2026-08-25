from __future__ import annotations


from rule_builder.rules import Has, True_, HasAll, HasAllCounts, HasAny, HasAnyCount, HasFromListUnique, Rule
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .world import EquilinoxWorld


def set_all_rules(world: EquilinoxWorld) -> None:
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_location_rules(world: EquilinoxWorld) -> None:

    return


def set_completion_condition(world: EquilinoxWorld) -> None:
    world.set_completion_rule(Has("Victory"))
