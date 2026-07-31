from __future__ import annotations
from rule_builder.rules import Has, True_, HasAll, HasAllCounts

from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

if TYPE_CHECKING:
    from .world import EarthWorld


def set_all_rules(world: EarthWorld) -> None:
    # In order for AP to generate an item layout that is actually possible for the player to complete,
    # we need to define rules for our Entrances and Locations.
    # Note: Regions do not have rules, the Entrances connecting them do!
    # We'll do entrances first, then locations, and then finally we set our victory condition.

    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: EarthWorld) -> None:
    # First, we need to actually grab our entrances. Luckily, there is a helper method for this.

    return


def set_all_location_rules(world: EarthWorld) -> None:
    # Location rules work no differently from Entrance rules.
    # Most of our locations are chests that can simply be opened by walking up to them.
    # Thus, their logical requirements are covered by the Entrance rules of the Entrances that were required to
    # reach the region that the chest sits in.
    # However, our two enemies work differently.
    # Entering the room with the enemy is not enough, you also need to have enough combat items to be able to defeat it.
    # So, we need to set requirements on the Locations themselves.
    # Since combat is a bit more complicated, we'll use this chance to cover some advanced access rule concepts.

    event_ecosystem = world.get_location("Angat Watershed Forest (25 pts)")
    world.set_rule(event_ecosystem, Has("Event Cards"))

    event_fauna = world.get_location("Green Tree Ant Claim")
    world.set_rule(event_fauna, Has("Event Cards"))

    set_ecosystem = world.get_location("Sakurajima (18 pts)")
    world.set_rule(set_ecosystem, Has("Event Cards"))

    set_fauna = world.get_location("Fire Salamander Claim")
    world.set_rule(set_fauna, Has("Event Cards"))

    victory = world.get_location("Game finished")
    world.set_rule(victory, HasAllCounts({"Sprout Storage": 1,
                                          "Germination": 1,
                                          "Progressive Starting Leaf": 4,
                                          "Progressive Score Cap": 4,
                                          "Progressive Green Call": 5,
                                          "Progressive Red Call": 3,
                                          "Progressive Blue Call": 3,
                                          "Progressive Yellow Call": 3}))
    return


def set_completion_condition(world: EarthWorld) -> None:
    # In our case, we went for the Victory event design pattern (see create_events() in locations.py).
    # So lets undo what we just did, and instead set the completion condition to:
    world.set_completion_rule(Has("Victory"))
