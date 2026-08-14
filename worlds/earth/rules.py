from __future__ import annotations

from rule_builder.rules import Has, True_, HasAll, HasAllCounts, HasAny, HasAnyCount, HasFromListUnique, Rule
from . import locations
from typing import TYPE_CHECKING

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

    return

def set_ecosystem_rules(world: EarthWorld) -> None:
    ecosystems = locations.get_ecosystem_locs()

    for ecosystem in ecosystems:
        rule = True_()

        if ecosystem.needs_events:
            rule = rule & Has("Event Cards")

        if ecosystem.red_calls > 0:
            rule = rule & HasAllCounts({"Progressive Red Call": ecosystem.red_calls, "Progressive Red Ability Activation": ecosystem.red_calls - 1})

        if ecosystem.blue_calls > 0:
            rule = rule & HasAllCounts({"Progressive Blue Call": ecosystem.blue_calls, "Progressive Blue Ability Activation": ecosystem.blue_calls - 1})

        if ecosystem.yellow_calls > 0:
            rule = rule & HasAllCounts({"Progressive Yellow Call": ecosystem.yellow_calls, "Progressive Yellow Ability Activation": ecosystem.yellow_calls - 1})

        if ecosystem.needed_cards > 0:
            calls = (ecosystem.needed_cards + 1) // 2 - 1
            rule = rule & Has("Progressive Green Call", count=calls)
            if ecosystem.red_calls < 2:
                if ecosystem.needed_cards > 8:
                    rule = rule & (HasAnyCount({"Progressive Red Call": 3, "Progressive Blue Call": 3})
                                   | HasAllCounts({"Progressive Red Call": 2, "Progressive Blue Call": 1})
                                   | HasAllCounts({"Progressive Red Call": 1, "Progressive Blue Call": 2}))
                elif ecosystem.needed_cards > 4:
                    rule = rule & (HasAnyCount({"Progressive Red Call": 2, "Progressive Blue Call": 2})
                                   | HasAllCounts({"Progressive Red Call": 1, "Progressive Blue Call": 1}))
                else:
                    rule = rule & HasAnyCount({"Progressive Red Call": 1, "Progressive Blue Call": 1})

        if world.options.kinder_card_logic:
            if ecosystem.name == "Antarctica":
                rule = rule & Has("Tableau Black Abilities")
            elif ecosystem.name == "Mount Kilimanjaro":
                rule = rule & HasAny("Terrain Abilities (Cheapening)", "Terrain Abilities (Scoring)", "Terrain Abilities (Replacement)")

        world.set_rule(world.get_location(locations.get_loc_name_from_eco(ecosystem)), rule)

def set_fauna_rules(world: EarthWorld) -> None:
    faunas = locations.get_fauna_locs()

    for fauna in faunas:
        rule = True_()

        if fauna.needs_events:
            rule = rule & Has("Event Cards")

        if fauna.red_calls > 0:
            rule = rule & HasAllCounts({"Progressive Red Call": fauna.red_calls,
                                        "Progressive Red Ability Activation": fauna.red_calls - 1})

        if fauna.blue_calls > 0:
            rule = rule & HasAllCounts({"Progressive Blue Call": fauna.blue_calls,
                                        "Progressive Blue Ability Activation": fauna.blue_calls - 1})

        if fauna.yellow_calls > 0:
            rule = rule & HasAllCounts({"Progressive Yellow Call": fauna.yellow_calls,
                                        "Progressive Yellow Ability Activation": fauna.yellow_calls - 1})

        if fauna.needed_cards > 0:
            calls = (fauna.needed_cards + 1) // 2 - 1
            rule = rule & Has("Progressive Green Call", count=calls)
            if fauna.red_calls < 2:
                if fauna.needed_cards > 8:
                    rule = rule & (HasAnyCount({"Progressive Red Call": 3, "Progressive Blue Call": 3})
                                   | HasAllCounts({"Progressive Red Call": 2, "Progressive Blue Call": 1})
                                   | HasAllCounts({"Progressive Red Call": 1, "Progressive Blue Call": 2}))
                elif fauna.needed_cards > 4:
                    rule = rule & (HasAnyCount({"Progressive Red Call": 2, "Progressive Blue Call": 2})
                                   | HasAllCounts({"Progressive Red Call": 1, "Progressive Blue Call": 1}))
                else:
                    rule = rule & HasAnyCount({"Progressive Red Call": 1, "Progressive Blue Call": 1})

        if world.options.kinder_card_logic:
            if fauna.name == "Brown Bear":
                rule = rule & HasAny("Terrain Abilities (Cheapening)", "Terrain Abilities (Scoring)", "Terrain Abilities (Replacement)")

        world.set_rule(world.get_location(locations.get_loc_name_from_fauna(fauna)), rule)

def set_all_location_rules(world: EarthWorld) -> None:

    set_ecosystem_rules(world)

    set_fauna_rules(world)

    points50 = world.get_location("Score 50 Points")
    points100 = world.get_location("Score 100 Points")
    points150 = world.get_location("Score 150 Points")
    points200 = world.get_location("Score 200 Points")

    world.set_rule(points50, HasAnyCount({"Personal Ecosystem": 1,
                                          "Terrain Abilities (Scoring)": 1,
                                          "Progressive Green Call": 3,
                                          "Progressive Starting Leaf": 3
                                          }))

    world.set_rule(points100, HasAllCounts({"Personal Ecosystem": 1,
                                            "Progressive Green Call": 2,
                                            "Progressive Starting Leaf": 2,
                                            "Progressive Sprout Storage Cap": 2,
                                            "Progressive Green Ability Activation": 2,
                                            "Event Cards": 1,
                                            "Progressive Score Cap": 1
                                            }))

    world.set_rule(points150, HasAllCounts({"Personal Ecosystem": 1,
                                            "Progressive Green Call": 3,
                                            "Progressive Starting Leaf": 2,
                                            "Progressive Sprout Storage Cap": 3,
                                            "Progressive Blue Call": 2,
                                            "Progressive Green Ability Activation": 2,
                                            "Event Cards": 1,
                                            "Terrain Abilities (Scoring)": 1,
                                            "Progressive Score Cap": 2
                                            }))

    world.set_rule(points200, HasAllCounts({"Personal Ecosystem": 1,
                                            "Progressive Green Call": 3,
                                            "Progressive Starting Leaf": 3,
                                            "Progressive Sprout Storage Cap": 3,
                                            "Progressive Blue Call": 2,
                                            "Progressive Red Call": 2,
                                            "Progressive Yellow Call": 2,
                                            "Progressive Green Ability Activation": 2,
                                            "Event Cards": 1,
                                            "Terrain Abilities (Scoring)": 1,
                                            "Germination": 1,
                                            "Progressive Score Cap": 3
                                            }))

    if world.options.kinder_card_logic:
        black_ability_locs = ["Play card Bamboo Forest",
                                "Play card Compost-filled Grounds",
                                "Play card African Baobab",
                                "Play card Volcanic Grounds",
                                "Play card Strangler Fig",
                                "Play card Giant Bearded Fig",
                                "Play card American Beech",
                                "Play card Red Gram",
                                "Play card Netted Rhodotus",
                                "Play card Tor-Grass",
                                "Play card Pomegranate Tree",
                                "Play card Flooded Delta",
                                "Play card White Snowdrop",
                                "Play card Indian Oyster",
                                "Play card Horn of Plenty",
                                "Play card Siberian Elm",
                                "Play card English Walnut",
                                "Play card Luxuriant Woodland",
                                "Play card Chernozem",
                                "Play card Chinese Elm",
                                "Play card Volcanic Ash Plain",
                                "Play card Monsoon Irrigated Plateau",
                                "Play card Sunny Hillside"]
        for loc in black_ability_locs:
            world.set_rule(world.get_location(loc), Has("Tableau Black Abilities"))

        scoring_brown_abilities = ["Play card Rainbow Mountain",
                                    "Play card Strait",
                                    "Play card Meadow",
                                    "Play card Forest Meadow",
                                    "Play card Volcanic Crater",
                                    "Play card Gigantic Island",
                                    "Play card Desert",
                                    "Play card Rain Forest",
                                    "Play card Mountain Forest",
                                    #"Play card Tropical Sierra",
                                    "Play card Mountain Ridge",
                                    "Play card Tropical Jungle",
                                    "Play card Cordillera",
                                    #"Play card Volcanic Island",
                                    "Play card Putrefied Land",
                                    "Play card Prairie",
                                    "Play card Permafrost",
                                    "Play card Badlands",
                                    "Play card Stream",
                                    "Play card Taiga",
                                    "Play card Pasture",
                                    "Play card Glacier",
                                    "Play card Crater",
                                    "Play card Blooming Land",
                                    "Play card Volcano",
                                    "Play card River",
                                    "Play card Cold Peaked Mount",
                                    "Play card Savanna",
                                    "Play card Jungle",
                                    "Play card Prominent Peak",
                                    "Play card Sub-Frigid Grassland",
                                    "Play card Mixed Forest",
                                    "Play card Lake",
                                    "Play card Plain",
                                    "Play card Blossoming Lands",
                                    "Play card Grassland",
                                    "Play card Swamp",
                                    "Play card Impoverished Land",
                                    "Play card Bayou",
                                    "Play card Cloud Forest",
                                    "Play card Scrubland",
                                    "Play card Redwood Forest",
                                    "Play card Canyon",
                                    "Play card Boreal Forest",
                                    "Play card Shrubland",
                                    "Play card Forest Edge",
                                    "Play card Floodplain",
                                    "Play card Wetland",
                                    "Play card Fertile Land",
                                    "Play card Beach",
                                    "Play card Lava Field",
                                    "Play card Tropical Forest",
                                    "Play card Rocky Mountains",
                                    "Play card Mineral-rich Land",
                                    "Play card Giant Forest"]
        for loc in scoring_brown_abilities:
            world.set_rule(world.get_location(loc), Has("Terrain Abilities (Scoring)"))

        cheapening_brown_abilities = ["Play card Organic Soil",
                                        "Play card Sand Dunes",
                                        "Play card Water Pools",
                                        "Play card Solidified Magma",
                                        "Play card Arable Land",
                                        "Play card Aridisol",
                                        "Play card Tundra",
                                        "Play card Clay Soil",
                                        "Play card Sandy Soil",
                                        "Play card Riverside",
                                        "Play card Alfisol",
                                        "Play card Fallen Sequoia"]
        for loc in cheapening_brown_abilities:
            world.set_rule(world.get_location(loc), Has("Terrain Abilities (Cheapening)"))

        replacement_brown_abilities = ["Play card Flatland", "Play card Alluvial Sediments", "Play card Lava Plain"]
        for loc in replacement_brown_abilities:
            world.set_rule(world.get_location(loc), Has("Terrain Abilities (Replacement)"))

        world.set_rule(world.get_location("Play card Volcanic Island"), Has("Event Cards") & Has("Terrain Abilities (Scoring)"))
        world.set_rule(world.get_location("Play card Cacao Tree"), Has("Event Cards"))
        world.set_rule(world.get_location("Play card Tropical Sierra"), Has("Event Cards") & Has("Terrain Abilities (Scoring)"))

    has_four_climates = HasFromListUnique(
        "Climate Unlock: Hemiboreal / Tropical Savanna",
        "Climate Unlock: Dry Winter Subtropical Highland / Tropical Rain Forest",
        "Climate Unlock: Tundra / Tropical Monsoon",
        "Climate Unlock: Marine West Coast / Mediterranean Cold Summer",
        "Climate Unlock: Arid / Humid Subtropical",
        "Climate Unlock: Subpolar Oceanic / Mediterranean Hot Summer",
        "Climate Unlock: Oceanic / Subtropical Highland",
        "Climate Unlock: Boreal / Ice Cap",
        "Climate Unlock: Hot Summer Continental / Desert",
        "Climate Unlock: Semi-Arid / Dry Winter Subpolar Oceanic",
        "Climate Unlock: Cold Arid Desert / Hot Steppe",
        "Climate Unlock: Cold Winter Continental / Temperate Hot Summer",
        count = 4)

    has_six_islands = HasFromListUnique(
        "Island Unlock: Fogo / Whakaari",
        "Island Unlock: Kauai / Vulcano",
        "Island Unlock: La Palma / Metis Shoal",
        "Island Unlock: Barren / Santorini",
        "Island Unlock: Kyushu / Jamaica",
        "Island Unlock: Lombok / Hawai'i",
        "Island Unlock: Deception / Nisyros",
        "Island Unlock: Iceland / Mo'orea",
        "Island Unlock: Nishinoshima / Luzon",
        "Island Unlock: Jan Mayen / Kunashir",
        "Island Unlock: Ross Island / Vancouver Island",
        "Island Unlock: Java Island / Madagascar Island",
        count = 6)

    has_needed_items_and_unlocks = HasAllCounts({
        "Progressive Sprout Storage Cap": 4,
        "Germination": 1,
        "Progressive Starting Leaf": 4,
        "Progressive Score Cap": 5,
        "Progressive Green Call": 6,
        "Progressive Red Call": 4,
        "Progressive Blue Call": 4,
        "Progressive Yellow Call": 4,
        "Progressive Green Ability Activation": 4,
        "Progressive Red Ability Activation": 5,
        "Progressive Blue Ability Activation": 5,
        "Progressive Yellow Ability Activation": 5,
        "Tableau Black Abilities": 1,
        "Terrain Abilities (Scoring)": 1,
        "Personal Ecosystem": 1
        })

    victory = world.get_location("Game finished")
    if world.options.flower_hunt:
        flowers_needed = world.options.flowers_required.value
        has_all_flowers = Has("Flower", count=flowers_needed)
        world.set_rule(victory, has_needed_items_and_unlocks & has_four_climates & has_six_islands & has_all_flowers)
    else:
        world.set_rule(victory, has_needed_items_and_unlocks & has_four_climates & has_six_islands)


def set_completion_condition(world: EarthWorld) -> None:
    # In our case, we went for the Victory event design pattern (see create_events() in locations.py).
    # So lets undo what we just did, and instead set the completion condition to:
    world.set_completion_rule(Has("Victory"))
