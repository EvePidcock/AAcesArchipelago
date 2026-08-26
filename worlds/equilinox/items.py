from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification
from Species import get_species

if TYPE_CHECKING:
    from .world import EquilinoxWorld

ITEM_NAME_TO_ID = {}

DEFAULT_ITEM_CLASSIFICATIONS = {}

species_unlock_items = []

def set_item_names_to_id():
    #ITEM_NAME_TO_ID = {}

    species = get_species()

    # Base Species Unlocks
    for thing in species:
        if thing.is_base_species():
            id = thing.id
            item_name = f"{thing.name} Permit"
            if thing.is_plant:
                id += 10000
            else:
                id += 11000
            ITEM_NAME_TO_ID[item_name] = id
            DEFAULT_ITEM_CLASSIFICATIONS[item_name] = ItemClassification.progression
            species_unlock_items.append(item_name)

    ITEM_NAME_TO_ID["Filler"] = 90000
    DEFAULT_ITEM_CLASSIFICATIONS["Filler"] = ItemClassification.filler

    #return ITEM_NAME_TO_ID

class EquilinoxItem(Item):
    game = "Equilinox"

def get_random_filler_item_name(world: EquilinoxWorld) -> str:
    filler_items = ["Filler"]
    return world.random.sample(filler_items, 1)[0]


def create_item_with_correct_classification(world: EquilinoxWorld, name: str) -> EquilinoxItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    return EquilinoxItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: EquilinoxWorld) -> None:
    item_pool: list[Item] = [

    ]

    for unlock in species_unlock_items:
        item_pool.append(world.create_item(unlock))



    # Filler items
    number_of_items = len(item_pool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    item_pool += [world.create_filler() for _ in range(needed_number_of_filler_items)]


    world.multiworld.itempool += item_pool
