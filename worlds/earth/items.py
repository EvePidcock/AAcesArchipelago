from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import EarthWorld

#these ids are sorta arbitrary rn? idk
ITEM_NAME_TO_ID = {
    "Progressive Green Call": 1001,
    "Progressive Red Call": 1002,
    "Progressive Blue Call": 1003,
    "Progressive Yellow Call": 1004,

    "Progressive Green Ability Activation": 1101,
    "Progressive Red Ability Activation": 1102,
    "Progressive Blue Ability Activation": 1103,
    "Progressive Yellow Ability Activation": 1104,
    "Tableau Black Abilities": 1105,
    "Terrain Abilities (Cheapening)": 1106,
    "Terrain Abilities (Scoring)": 1107,
    "Terrain Abilities (Replacement)": 1108,

    "Event Cards": 2001,
    "Progressive Sprout Storage Cap": 2002,
    "Germination": 2003,
    "Personal Ecosystem": 2004,

    "Progressive Starting Soil": 3001,
    "Progressive Starting Sprout": 3002,
    "Progressive Starting Seed": 3003,
    "Progressive Starting Leaf": 3004,
    "Progressive Starting Card Draw": 3005,

    "Progressive Score Cap": 4001,

    "Island Unlock: Fogo / Whakaari": 5001,
    "Island Unlock: Kauai / Vulcano": 5002,
    "Island Unlock: La Palma / Metis Shoal": 5003,
    "Island Unlock: Barren / Santorini": 5004,
    "Island Unlock: Kyushu / Jamaica": 5005,
    "Island Unlock: Lombok / Hawai'i": 5006,
    "Island Unlock: Deception / Nisyros": 5007,
    "Island Unlock: Iceland / Mo'orea": 5008,
    "Island Unlock: Nishinoshima / Luzon": 5009,
    "Island Unlock: Jan Mayen / Kunashir": 5010,
    "Island Unlock: Ross Island / Vancouver Island": 5011,
    "Island Unlock: Java Island / Madagascar Island": 5012,

    "Climate Unlock: Hemiboreal / Tropical Savanna": 5101,
    "Climate Unlock: Dry Winter Subtropical Highland / Tropical Rain Forest": 5102,
    "Climate Unlock: Tundra / Tropical Monsoon": 5103,
    "Climate Unlock: Marine West Coast / Mediterranean Cold Summer": 5104,
    "Climate Unlock: Arid / Humid Subtropical": 5105,
    "Climate Unlock: Subpolar Oceanic / Mediterranean Hot Summer": 5106,
    "Climate Unlock: Oceanic / Subtropical Highland": 5107,
    "Climate Unlock: Boreal / Ice Cap": 5108,
    "Climate Unlock: Hot Summer Continental / Desert": 5109,
    "Climate Unlock: Semi-Arid / Dry Winter Subpolar Oceanic": 5110,
    "Climate Unlock: Cold Arid Desert / Hot Steppe": 5111,
    "Climate Unlock: Cold Winter Continental / Temperate Hot Summer": 5112,

    "Flower": 6001,

    "A Cool Bird": 9001,
    "A Neat Mushroom": 9002,
    "A Pretty Tree": 9003,
    "A Lush Bush": 9004,
    "A Raging River": 9005,
    "A Little Bug": 9006
}

DEFAULT_ITEM_CLASSIFICATIONS = {
    "Progressive Green Call": ItemClassification.progression,
    "Progressive Red Call": ItemClassification.progression,
    "Progressive Blue Call": ItemClassification.progression,
    "Progressive Yellow Call": ItemClassification.progression,

    "Progressive Green Ability Activation": ItemClassification.progression,
    "Progressive Red Ability Activation": ItemClassification.progression,
    "Progressive Blue Ability Activation": ItemClassification.progression,
    "Progressive Yellow Ability Activation": ItemClassification.progression,

    "Tableau Black Abilities": ItemClassification.progression,
    "Terrain Abilities (Cheapening)": ItemClassification.progression,
    "Terrain Abilities (Scoring)": ItemClassification.progression,
    "Terrain Abilities (Replacement)": ItemClassification.progression,

    "Event Cards": ItemClassification.progression | ItemClassification.useful,
    "Progressive Sprout Storage Cap": ItemClassification.progression,
    "Germination": ItemClassification.progression | ItemClassification.useful,
    "Personal Ecosystem": ItemClassification.progression | ItemClassification.useful,

    "Progressive Starting Soil": ItemClassification.useful,
    "Progressive Starting Sprout": ItemClassification.useful,
    "Progressive Starting Seed": ItemClassification.useful,
    "Progressive Starting Leaf": ItemClassification.progression,
    "Progressive Starting Card Draw": ItemClassification.useful,

    "Progressive Score Cap": ItemClassification.progression,

    "Island Unlock: Fogo / Whakaari": ItemClassification.progression,
    "Island Unlock: Kauai / Vulcano": ItemClassification.progression,
    "Island Unlock: La Palma / Metis Shoal": ItemClassification.progression,
    "Island Unlock: Barren / Santorini": ItemClassification.progression,
    "Island Unlock: Kyushu / Jamaica": ItemClassification.progression,
    "Island Unlock: Lombok / Hawai'i": ItemClassification.progression,
    "Island Unlock: Deception / Nisyros": ItemClassification.progression,
    "Island Unlock: Iceland / Mo'orea": ItemClassification.progression,
    "Island Unlock: Nishinoshima / Luzon": ItemClassification.progression,
    "Island Unlock: Jan Mayen / Kunashir": ItemClassification.progression,
    "Island Unlock: Ross Island / Vancouver Island": ItemClassification.progression,
    "Island Unlock: Java Island / Madagascar Island": ItemClassification.progression,

    "Climate Unlock: Hemiboreal / Tropical Savanna": ItemClassification.progression,
    "Climate Unlock: Dry Winter Subtropical Highland / Tropical Rain Forest": ItemClassification.progression,
    "Climate Unlock: Tundra / Tropical Monsoon": ItemClassification.progression,
    "Climate Unlock: Marine West Coast / Mediterranean Cold Summer": ItemClassification.progression,
    "Climate Unlock: Arid / Humid Subtropical": ItemClassification.progression,
    "Climate Unlock: Subpolar Oceanic / Mediterranean Hot Summer": ItemClassification.progression,
    "Climate Unlock: Oceanic / Subtropical Highland": ItemClassification.progression,
    "Climate Unlock: Boreal / Ice Cap": ItemClassification.progression,
    "Climate Unlock: Hot Summer Continental / Desert": ItemClassification.progression,
    "Climate Unlock: Semi-Arid / Dry Winter Subpolar Oceanic": ItemClassification.progression,
    "Climate Unlock: Cold Arid Desert / Hot Steppe": ItemClassification.progression,
    "Climate Unlock: Cold Winter Continental / Temperate Hot Summer": ItemClassification.progression,

    "Flower": ItemClassification.progression,

    "A Cool Bird": ItemClassification.filler,
    "A Neat Mushroom": ItemClassification.filler,
    "A Pretty Tree": ItemClassification.filler,
    "A Lush Bush": ItemClassification.filler,
    "A Raging River": ItemClassification.filler,
    "A Little Bug": ItemClassification.filler
}

class EarthItem(Item):
    game = "Earth"

def get_random_filler_item_name(world: EarthWorld) -> str:
    filler_items = ["A Cool Bird", "A Neat Mushroom", "A Pretty Tree", "A Lush Bush", "A Raging River", "A Little Bug"]
    return world.random.sample(filler_items, 1)[0]


def create_item_with_correct_classification(world: EarthWorld, name: str) -> EarthItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    return EarthItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: EarthWorld) -> None:
    item_pool: list[Item] = [
        world.create_item("Progressive Green Call"),
        world.create_item("Progressive Green Call"),
        world.create_item("Progressive Green Call"),
        world.create_item("Progressive Green Call"),
        world.create_item("Progressive Green Call"),
        world.create_item("Progressive Green Call"),
        world.create_item("Progressive Green Call"),
        world.create_item("Progressive Green Call"),
        world.create_item("Progressive Green Call"),
        world.create_item("Progressive Red Call"),
        world.create_item("Progressive Red Call"),
        world.create_item("Progressive Red Call"),
        world.create_item("Progressive Red Call"),
        world.create_item("Progressive Red Call"),
        world.create_item("Progressive Red Call"),
        world.create_item("Progressive Red Call"),
        world.create_item("Progressive Blue Call"),
        world.create_item("Progressive Blue Call"),
        world.create_item("Progressive Blue Call"),
        world.create_item("Progressive Blue Call"),
        world.create_item("Progressive Blue Call"),
        world.create_item("Progressive Blue Call"),
        world.create_item("Progressive Blue Call"),
        world.create_item("Progressive Yellow Call"),
        world.create_item("Progressive Yellow Call"),
        world.create_item("Progressive Yellow Call"),
        world.create_item("Progressive Yellow Call"),
        world.create_item("Progressive Yellow Call"),
        world.create_item("Progressive Yellow Call"),
        world.create_item("Progressive Yellow Call"),

        world.create_item("Progressive Green Ability Activation"),
        world.create_item("Progressive Green Ability Activation"),
        world.create_item("Progressive Green Ability Activation"),
        world.create_item("Progressive Green Ability Activation"),
        world.create_item("Progressive Green Ability Activation"),
        world.create_item("Progressive Green Ability Activation"),
        world.create_item("Progressive Green Ability Activation"),
        world.create_item("Progressive Green Ability Activation"),
        world.create_item("Progressive Green Ability Activation"),
        world.create_item("Progressive Green Ability Activation"),
        world.create_item("Progressive Green Ability Activation"),

        world.create_item("Progressive Red Ability Activation"),
        world.create_item("Progressive Red Ability Activation"),
        world.create_item("Progressive Red Ability Activation"),
        world.create_item("Progressive Red Ability Activation"),
        world.create_item("Progressive Red Ability Activation"),
        world.create_item("Progressive Red Ability Activation"),
        world.create_item("Progressive Red Ability Activation"),
        world.create_item("Progressive Red Ability Activation"),
        world.create_item("Progressive Red Ability Activation"),
        world.create_item("Progressive Red Ability Activation"),
        world.create_item("Progressive Red Ability Activation"),
        world.create_item("Progressive Red Ability Activation"),
        world.create_item("Progressive Red Ability Activation"),
        world.create_item("Progressive Red Ability Activation"),
        world.create_item("Progressive Red Ability Activation"),
        world.create_item("Progressive Red Ability Activation"),
        world.create_item("Progressive Red Ability Activation"),
        world.create_item("Progressive Red Ability Activation"),

        world.create_item("Progressive Blue Ability Activation"),
        world.create_item("Progressive Blue Ability Activation"),
        world.create_item("Progressive Blue Ability Activation"),
        world.create_item("Progressive Blue Ability Activation"),
        world.create_item("Progressive Blue Ability Activation"),
        world.create_item("Progressive Blue Ability Activation"),
        world.create_item("Progressive Blue Ability Activation"),
        world.create_item("Progressive Blue Ability Activation"),
        world.create_item("Progressive Blue Ability Activation"),
        world.create_item("Progressive Blue Ability Activation"),
        world.create_item("Progressive Blue Ability Activation"),
        world.create_item("Progressive Blue Ability Activation"),
        world.create_item("Progressive Blue Ability Activation"),
        world.create_item("Progressive Blue Ability Activation"),
        world.create_item("Progressive Blue Ability Activation"),
        world.create_item("Progressive Blue Ability Activation"),
        world.create_item("Progressive Blue Ability Activation"),
        world.create_item("Progressive Blue Ability Activation"),

        world.create_item("Progressive Yellow Ability Activation"),
        world.create_item("Progressive Yellow Ability Activation"),
        world.create_item("Progressive Yellow Ability Activation"),
        world.create_item("Progressive Yellow Ability Activation"),
        world.create_item("Progressive Yellow Ability Activation"),
        world.create_item("Progressive Yellow Ability Activation"),
        world.create_item("Progressive Yellow Ability Activation"),
        world.create_item("Progressive Yellow Ability Activation"),
        world.create_item("Progressive Yellow Ability Activation"),
        world.create_item("Progressive Yellow Ability Activation"),
        world.create_item("Progressive Yellow Ability Activation"),
        world.create_item("Progressive Yellow Ability Activation"),
        world.create_item("Progressive Yellow Ability Activation"),
        world.create_item("Progressive Yellow Ability Activation"),
        world.create_item("Progressive Yellow Ability Activation"),
        world.create_item("Progressive Yellow Ability Activation"),
        world.create_item("Progressive Yellow Ability Activation"),
        world.create_item("Progressive Yellow Ability Activation"),

        world.create_item("Tableau Black Abilities"),
        world.create_item("Terrain Abilities (Cheapening)"),
        world.create_item("Terrain Abilities (Scoring)"),
        world.create_item("Terrain Abilities (Replacement)"),

        world.create_item("Event Cards"),
        world.create_item("Germination"),

        world.create_item("Progressive Sprout Storage Cap"),
        world.create_item("Progressive Sprout Storage Cap"),
        world.create_item("Progressive Sprout Storage Cap"),
        world.create_item("Progressive Sprout Storage Cap"),
        world.create_item("Progressive Sprout Storage Cap"),
        world.create_item("Progressive Sprout Storage Cap"),
        world.create_item("Progressive Sprout Storage Cap"),
        world.create_item("Progressive Sprout Storage Cap"),
        world.create_item("Progressive Sprout Storage Cap"),
        world.create_item("Progressive Sprout Storage Cap"),
        world.create_item("Progressive Sprout Storage Cap"),
        world.create_item("Progressive Sprout Storage Cap"),

        world.create_item("Progressive Starting Soil"),
        world.create_item("Progressive Starting Soil"),
        world.create_item("Progressive Starting Soil"),
        world.create_item("Progressive Starting Soil"),
        world.create_item("Progressive Starting Soil"),
        world.create_item("Progressive Starting Soil"),
        world.create_item("Progressive Starting Soil"),
        world.create_item("Progressive Starting Soil"),
        world.create_item("Progressive Starting Sprout"),
        world.create_item("Progressive Starting Sprout"),
        world.create_item("Progressive Starting Sprout"),
        world.create_item("Progressive Starting Sprout"),
        world.create_item("Progressive Starting Sprout"),
        world.create_item("Progressive Starting Seed"),
        world.create_item("Progressive Starting Seed"),
        world.create_item("Progressive Starting Seed"),
        world.create_item("Progressive Starting Leaf"),
        world.create_item("Progressive Starting Leaf"),
        world.create_item("Progressive Starting Leaf"),
        world.create_item("Progressive Starting Leaf"),
        world.create_item("Progressive Starting Leaf"),
        world.create_item("Progressive Starting Card Draw"),
        world.create_item("Progressive Starting Card Draw"),
        world.create_item("Progressive Starting Card Draw"),
        world.create_item("Progressive Starting Card Draw"),
        world.create_item("Progressive Starting Card Draw"),

        world.create_item("Progressive Score Cap"),
        world.create_item("Progressive Score Cap"),
        world.create_item("Progressive Score Cap"),
        world.create_item("Progressive Score Cap"),
        world.create_item("Progressive Score Cap"),
        world.create_item("Progressive Score Cap"),
        world.create_item("Progressive Score Cap"),

        world.create_item("Island Unlock: Fogo / Whakaari"),
        world.create_item("Island Unlock: Kauai / Vulcano"),
        world.create_item("Island Unlock: La Palma / Metis Shoal"),
        world.create_item("Island Unlock: Barren / Santorini"),
        world.create_item("Island Unlock: Kyushu / Jamaica"),
        world.create_item("Island Unlock: Lombok / Hawai'i"),
        world.create_item("Island Unlock: Deception / Nisyros"),
        world.create_item("Island Unlock: Iceland / Mo'orea"),
        world.create_item("Island Unlock: Nishinoshima / Luzon"),
        world.create_item("Island Unlock: Jan Mayen / Kunashir"),
        world.create_item("Island Unlock: Ross Island / Vancouver Island"),
        world.create_item("Island Unlock: Java Island / Madagascar Island"),

        world.create_item("Climate Unlock: Hemiboreal / Tropical Savanna"),
        world.create_item("Climate Unlock: Dry Winter Subtropical Highland / Tropical Rain Forest"),
        world.create_item("Climate Unlock: Tundra / Tropical Monsoon"),
        world.create_item("Climate Unlock: Marine West Coast / Mediterranean Cold Summer"),
        world.create_item("Climate Unlock: Arid / Humid Subtropical"),
        world.create_item("Climate Unlock: Subpolar Oceanic / Mediterranean Hot Summer"),
        world.create_item("Climate Unlock: Oceanic / Subtropical Highland"),
        world.create_item("Climate Unlock: Boreal / Ice Cap"),
        world.create_item("Climate Unlock: Hot Summer Continental / Desert"),
        world.create_item("Climate Unlock: Semi-Arid / Dry Winter Subpolar Oceanic"),
        world.create_item("Climate Unlock: Cold Arid Desert / Hot Steppe"),
        world.create_item("Climate Unlock: Cold Winter Continental / Temperate Hot Summer"),
    ]

    starting_ability_items = [
        world.create_item("Progressive Green Call"),
        #world.create_item("Progressive Red Call"),
        #world.create_item("Progressive Blue Call"),
        #world.create_item("Progressive Yellow Call"),

        #world.create_item("Progressive Green Ability Activation"),
        world.create_item("Progressive Red Ability Activation"),
        world.create_item("Progressive Blue Ability Activation"),
        world.create_item("Progressive Yellow Ability Activation")
    ]

    if world.options.starting_leaf:
        starting_ability_items.append(world.create_item("Progressive Starting Leaf"))

    if world.options.starting_seed:
        starting_ability_items.append(world.create_item("Progressive Starting Seed"))

    if world.options.starting_sprout_storage:
        starting_ability_items.append(world.create_item("Progressive Sprout Storage Cap"))

    if world.options.starting_personal_ecosystem:
        starting_ability_items.append(world.create_item("Personal Ecosystem"))
    else:
        item_pool.append(world.create_item("Personal Ecosystem"))

    for item in starting_ability_items:
        world.push_precollected(item)

    # Flowers
    if world.options.flower_hunt:
        flowers_needed = world.options.flowers_required.value
        flowers_total = max(flowers_needed, world.options.flowers_total.value)
        item_pool += [world.create_item("Flower") for _ in range(flowers_total)]

    # Filler items
    number_of_items = len(item_pool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    item_pool += [world.create_filler() for _ in range(needed_number_of_filler_items)]


    world.multiworld.itempool += item_pool
