from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification
from . import SpeciesUtils, Tasks, Evolution

if TYPE_CHECKING:
    from .world import EquilinoxWorld

ITEM_NAME_TO_ID = {}

DEFAULT_ITEM_CLASSIFICATIONS = {}

species_unlock_items = []

def set_item_names_to_id():
    #ITEM_NAME_TO_ID = {}

    all_species = SpeciesUtils.all_species

    # Base Species Unlocks
    for species in all_species:
        if species.is_base_species():

            id = species.id
            item_name = f"{species.name} Permit"
            if species.is_plant:
                id += 10000
            else:
                id += 11000
            ITEM_NAME_TO_ID[item_name] = id
            DEFAULT_ITEM_CLASSIFICATIONS[item_name] = ItemClassification.progression
            species_unlock_items.append(item_name)

    ITEM_NAME_TO_ID["100 dp"] = 80001
    ITEM_NAME_TO_ID["500 dp"] = 80005

    ITEM_NAME_TO_ID["1,000 dp"] = 80010
    ITEM_NAME_TO_ID["2,500 dp"] = 80025
    ITEM_NAME_TO_ID["5,000 dp"] = 80050
    ITEM_NAME_TO_ID["7,500 dp"] = 80075

    ITEM_NAME_TO_ID["10,000 dp"] = 80100
    ITEM_NAME_TO_ID["25,000 dp"] = 80250
    ITEM_NAME_TO_ID["50,000 dp"] = 80500
    ITEM_NAME_TO_ID["75,000 dp"] = 80750

    ITEM_NAME_TO_ID["100,000 dp"] = 81000

    DEFAULT_ITEM_CLASSIFICATIONS["100 dp"] = ItemClassification.filler
    DEFAULT_ITEM_CLASSIFICATIONS["500 dp"] = ItemClassification.filler

    DEFAULT_ITEM_CLASSIFICATIONS["1,000 dp"] = ItemClassification.useful | ItemClassification.filler
    DEFAULT_ITEM_CLASSIFICATIONS["2,500 dp"] = ItemClassification.useful | ItemClassification.filler
    DEFAULT_ITEM_CLASSIFICATIONS["5,000 dp"] = ItemClassification.useful | ItemClassification.filler
    DEFAULT_ITEM_CLASSIFICATIONS["7,500 dp"] = ItemClassification.useful | ItemClassification.filler

    DEFAULT_ITEM_CLASSIFICATIONS["10,000 dp"] = ItemClassification.progression_skip_balancing
    DEFAULT_ITEM_CLASSIFICATIONS["25,000 dp"] = ItemClassification.progression_skip_balancing
    DEFAULT_ITEM_CLASSIFICATIONS["50,000 dp"] = ItemClassification.progression_skip_balancing
    DEFAULT_ITEM_CLASSIFICATIONS["75,000 dp"] = ItemClassification.progression_skip_balancing

    DEFAULT_ITEM_CLASSIFICATIONS["100,000 dp"] = ItemClassification.useful

    DEFAULT_ITEM_CLASSIFICATIONS["Filler"] = 90001
    DEFAULT_ITEM_CLASSIFICATIONS["Filler"] = ItemClassification.filler

    #return ITEM_NAME_TO_ID

class EquilinoxItem(Item):
    game = "Equilinox"

def get_random_filler_item_name(world: EquilinoxWorld) -> str:
    filler_items = ["100 dp", "500 dp", "1,000 dp", "2,500 dp", "5,000 dp", "7,500 dp", "10,000 dp"]
    weights =      [ 10,       15,       5,          4,          3,          2,          1         ]
    return world.random.choices(filler_items, weights=weights, k=1)[0]


def create_item_with_correct_classification(world: EquilinoxWorld, name: str) -> EquilinoxItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    return EquilinoxItem(name, classification, ITEM_NAME_TO_ID[name], world.player)

def get_nearest_money_item(world: EquilinoxWorld, amt: int) -> EquilinoxItem:
    if amt >= 100000:
        return world.create_item("100,000 dp")
    elif amt >= 75000:
        return world.create_item("75,000 dp")
    elif amt >= 50000:
        return world.create_item("50,000 dp")
    elif amt >= 25000:
        return world.create_item("25,000 dp")
    elif amt >= 10000:
        return world.create_item("10,000 dp")
    elif amt >= 7500:
        return world.create_item("7,500 dp")
    elif amt >= 5000:
        return world.create_item("5,000 dp")
    elif amt >= 2500:
        return world.create_item("2,500 dp")
    elif amt >= 1000:
        return world.create_item("1,000 dp")
    elif amt >= 500:
        return world.create_item("500 dp")
    else:
        return world.create_item("100 dp")

def create_all_items(world: EquilinoxWorld) -> None:
    item_pool: list[Item] = [

    ]

    for unlock in species_unlock_items:
        if unlock == "Grass Tuft Permit": continue
        item_pool.append(world.create_item(unlock))

    if world.options.money_sanity:
        for task in Tasks.all_tasks:
            item_pool.append(get_nearest_money_item(world, task.cash_reward))


    # Filler items
    number_of_items = len(item_pool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    item_pool += [world.create_filler() for _ in range(needed_number_of_filler_items)]


    world.multiworld.itempool += item_pool
