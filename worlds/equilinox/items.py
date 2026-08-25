from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import EquilinoxWorld

#these ids are sorta arbitrary rn? idk
ITEM_NAME_TO_ID = {

}

DEFAULT_ITEM_CLASSIFICATIONS = {

}

class EquilinoxItem(Item):
    game = "Equilinox"

def get_random_filler_item_name(world: EquilinoxWorld) -> str:
    filler_items = ["A Cool Bird", "A Neat Mushroom", "A Pretty Tree", "A Lush Bush", "A Raging River", "A Little Bug"]
    return world.random.sample(filler_items, 1)[0]


def create_item_with_correct_classification(world: EquilinoxWorld, name: str) -> EquilinoxItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    return EquilinoxItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: EquilinoxWorld) -> None:
    item_pool: list[Item] = [

    ]



    # Filler items
    number_of_items = len(item_pool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    item_pool += [world.create_filler() for _ in range(needed_number_of_filler_items)]


    world.multiworld.itempool += item_pool
