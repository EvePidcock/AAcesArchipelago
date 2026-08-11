from __future__ import annotations
from rule_builder.rules import Has, True_, HasAll, HasAllCounts, HasAny, HasAnyCount, HasFromListUnique

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

    condor = world.get_location("Andean Condor Claim")
    gorilla = world.get_location("Mountain Gorilla Claim")
    mole = world.get_location("European Mole Claim")
    worm = world.get_location("Earthworm Claim")
    eagle = world.get_location("Bald Eagle Claim")
    woodpecker = world.get_location("Pale-Billed Woodpecker Claim")
    marmot = world.get_location("Yellow-Bellied Marmot Claim")
    squirrel = world.get_location("Red Squirrel Claim")

    world.set_rule(condor, HasAllCounts({"Progressive Yellow Call": 3, "Progressive Yellow Ability Activation": 2}))
    world.set_rule(gorilla, HasAllCounts({"Progressive Yellow Call": 2, "Progressive Yellow Ability Activation": 1, "Progressive Blue Call": 2, "Progressive Blue Ability Activation": 1}))
    world.set_rule(mole, HasAllCounts({"Progressive Red Call": 3, "Progressive Red Ability Activation": 2}))
    world.set_rule(worm, HasAllCounts({"Progressive Red Call": 3, "Progressive Red Ability Activation": 2}))
    world.set_rule(eagle, HasAllCounts({"Progressive Yellow Call": 2, "Progressive Yellow Ability Activation": 1}))
    world.set_rule(woodpecker, HasAllCounts({"Progressive Yellow Call": 2, "Progressive Yellow Ability Activation": 1}))
    world.set_rule(marmot, HasAllCounts({"Progressive Blue Call": 3, "Progressive Blue Ability Activation": 2}))
    world.set_rule(squirrel, HasAllCounts({"Progressive Blue Call": 2, "Progressive Blue Ability Activation": 1}))

    canopies = world.get_location("Bwindi Impenetrable Forest (18 pts)")
    all_cubes = world.get_location("Tongass National Forest (18 pts)")
    soil = world.get_location("Great Plains (24 pts)")
    compost = world.get_location("Amazon Rain Forest (24 pts)")
    cards = world.get_location("Borneo Lowland Rain Forest (24 pts)")
    growth = world.get_location("Madagascar Humid Canopy (18 pts)")
    cubes = world.get_location("Tai Poutini National Park (18 pts)")

    world.set_rule(canopies, HasAllCounts({"Progressive Yellow Call": 2, "Progressive Yellow Ability Activation": 2}))
    world.set_rule(soil, HasAllCounts({"Progressive Red Call": 3, "Progressive Red Ability Activation": 2}))
    world.set_rule(compost, HasAllCounts({"Progressive Red Call": 3, "Progressive Red Ability Activation": 2}))
    world.set_rule(growth, HasAllCounts({"Progressive Yellow Call": 2, "Progressive Yellow Ability Activation": 2}))
    world.set_rule(cards, HasAllCounts({"Progressive Yellow Call": 2, "Progressive Yellow Ability Activation": 2}))
    world.set_rule(all_cubes, HasAllCounts({"Progressive Blue Call": 3, "Progressive Blue Ability Activation": 2}))
    world.set_rule(cubes, HasAllCounts({"Progressive Blue Call": 2, "Progressive Blue Ability Activation": 2}))

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

    needs_eight_cards_played = ["Wood Duck Claim",
                                "Siamese Rhinoceros Beetle Claim",
                                "Hedgehog Claim",
                                "Dung Beetle Claim",
                                "Arctic Fox Claim",
                                "American Alligator Claim",
                                "Sri Lankan Leopard Claim",
                                "Atlantic Puffin Claim",
                                "Yellow Cheeked Gibbon Claim",
                                "Hippopotamus Claim",
                                "Mountain Lion Claim",
                                "Plains Zebra Claim",
                                "Northern Giraffe Claim",
                                "Cairns Birdwing Butterfly Claim",
                                "Red Squirrel Claim",
                                "Western Moose Claim",
                                "Seven-Spotted Ladybug Claim",
                                "Black Wildebeest Claim",
                                "Fire Salamander Claim",
                                "Indonesian Pit Viper Claim",
                                "Margay Claim",
                                "Western Honeybee Claim",
                                "Pale-Billed Woodpecker Claim"]
    needs_four_plus_cards_played = ["Red Deer Claim",
                                    "American Bison Claim",
                                    "Kingfisher Claim",
                                    "Echidna Claim",
                                    "Siberian Tiger Claim",
                                    "Bornean Orangutan Claim",
                                    "Lubber Grasshopper Claim",
                                    "Wild Boar Claim",
                                    "Brown Bear Claim",
                                    "Green Iguana Claim",
                                    "Bald Eagle Claim",
                                    "African Bush Elephant Claim",
                                    "Praying Mantis Claim",
                                    "King Penguin Claim",
                                    "Panther Chameleon Claim",
                                    "Mountain Gorilla Claim",
                                    "Grey Wolf Claim",
                                    "Brown-Throated Sloth Claim",
                                    "Yellow-Bellied Marmot Claim"]
    ecosystems_that_need_cards_played = [key for key, value in world.location_name_to_id.items() if (30000 < value < 40000)]
    ecosystems_that_need_cards_played.remove("Great Plains (24 pts)")
    ecosystems_that_need_cards_played.remove("Amazon Rain Forest (24 pts)")
    ecosystems_that_need_cards_played.remove("Borneo Lowland Rain Forest (24 pts)")
    ecosystems_that_need_cards_played.remove("Angat Watershed Forest (25 pts)")

    for loc in ecosystems_that_need_cards_played:
        world.set_rule(world.get_location(loc), HasAllCounts({"Progressive Green Call": 3}))

    for loc in needs_eight_cards_played:
        world.set_rule(world.get_location(loc), HasAllCounts({"Progressive Green Call": 3}))

    for loc in needs_four_plus_cards_played:
        world.set_rule(world.get_location(loc), HasAllCounts({"Progressive Green Call": 2}))

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
                                "Play card Sunny Hillside",
                                "Antarctica (18 pts)"]
        for loc in black_ability_locs:
            world.set_rule(world.get_location(loc), Has("Tableau Black Abilities"))

        world.set_rule(world.get_location("Brown Bear Claim"), HasAny("Terrain Abilities (Cheapening)", "Terrain Abilities (Scoring)", "Terrain Abilities (Replacement)"))
        world.set_rule(world.get_location("Mount Kilimanjaro (20 pts)"), HasAny("Terrain Abilities (Cheapening)", "Terrain Abilities (Scoring)", "Terrain Abilities (Replacement)"))

        scoring_brown_abilities = ["Play card Rainbow Mountain",
                                    "Play card Strait",
                                    "Play card Meadow",
                                    "Play card Forest Meadow",
                                    "Play card Volcanic Crater",
                                    "Play card Gigantic Island",
                                    "Play card Desert",
                                    "Play card Rain Forest",
                                    "Play card Mountain Forest",
                                    "Play card Tropical Sierra",
                                    "Play card Mountain Ridge",
                                    "Play card Tropical Jungle",
                                    "Play card Cordillera",
                                    "Play card Volcanic Island",
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

        world.set_rule(world.get_location("Play card Volcanic Island"), Has("Event Cards"))
        world.set_rule(world.get_location("Play card Cacao Tree"), Has("Event Cards"))
        world.set_rule(world.get_location("Play card Tropical Sierra"), Has("Event Cards"))

    has_four_climates = HasFromListUnique("Climate Unlock: Hemiboreal / Tropical Savanna",
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
                            "Climate Unlock: Cold Winter Continental / Temperate Hot Summer", count = 4)

    has_six_islands = HasFromListUnique("Island Unlock: Fogo / Whakaari",
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
                           "Island Unlock: Java Island / Madagascar Island", count = 6)

    has_needed_items_and_unlocks = HasAllCounts({"Progressive Sprout Storage Cap": 4,
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
