from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import EarthWorld

# Every item must have a unique integer ID associated with it.
# We will have a lookup from item name to ID here that, in world.py, we will import and bind to the world class.
# Even if an item doesn't exist on specific options, it must be present in this lookup.

#these ids are sorta arbitrary rn? idk
ITEM_NAME_TO_ID = {
    "Progressive Green Call": 1001,
    "Progressive Red Call": 1002,
    "Progressive Blue Call": 1003,
    "Progressive Yellow Call": 1004,

    "Event Cards": 2001,
    "Sprout Storage": 2002,
    "Germination": 2003,

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

    "Filler": 9001
}

# Items should have a defined default classification.
# In our case, we will make a dictionary from item name to classification.
DEFAULT_ITEM_CLASSIFICATIONS = {
    "Progressive Green Call": ItemClassification.progression,
    "Progressive Red Call": ItemClassification.progression,
    "Progressive Blue Call": ItemClassification.progression,
    "Progressive Yellow Call": ItemClassification.progression,

    "Event Cards": ItemClassification.progression,
    "Sprout Storage": ItemClassification.progression | ItemClassification.useful,
    "Germination": ItemClassification.progression | ItemClassification.useful,

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

    "Filler": ItemClassification.filler,
}


# Each Item instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Item class and override the "game" field.
class EarthItem(Item):
    game = "Earth"


# Ontop of our regular itempool, our world must be able to create arbitrary amounts of filler as requested by core.
# To do this, it must define a function called world.get_filler_item_name(), which we will define in world.py later.
# For now, let's make a function that returns the name of a random filler item here in items.py.
def get_random_filler_item_name(world: EarthWorld) -> str:

    return "Filler"


def create_item_with_correct_classification(world: EarthWorld, name: str) -> EarthItem:
    # Our world class must have a create_item() function that can create any of our items by name at any time.
    # So, we make this helper function that creates the item by name with the correct classification.
    # Note: This function's content could just be the contents of world.create_item in world.py directly,
    # but it seemed nicer to have it in its own function over here in items.py.
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]

    # It is perfectly normal and valid for an item's classification to differ based on the player's options.
    # In our case, Health Upgrades are only relevant to logic (and thus labeled as "progression") in hard mode.
    #if name == "Health Upgrade" and world.options.hard_mode:
    #    classification = ItemClassification.progression

    return EarthItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


# With those two helper functions defined, let's now get to actually creating and submitting our itempool.
def create_all_items(world: EarthWorld) -> None:
    # This is the function in which we will create all the items that this world submits to the multiworld item pool.
    # There must be exactly as many items as there are locations.
    # In our case, there are either six or seven locations.
    # We must make sure that when there are six locations, there are six items,
    # and when there are seven locations, there are seven items.

    # Creating items should generally be done via the world's create_item method.
    # First, we create a list containing all the items that always exist.

    itempool: list[Item] = [
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

        world.create_item("Event Cards"),
        world.create_item("Sprout Storage"),
        world.create_item("Germination"),

        world.create_item("Progressive Starting Soil"),
        world.create_item("Progressive Starting Soil"),
        world.create_item("Progressive Starting Soil"),
        world.create_item("Progressive Starting Soil"),
        world.create_item("Progressive Starting Sprout"),
        world.create_item("Progressive Starting Sprout"),
        world.create_item("Progressive Starting Sprout"),
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

    # Archipelago requires that each world submits as many locations as it submits items.
    # This is where we can use our filler and trap items.
    # APQuest has two of these: The Confetti Cannon and the Math Trap.
    # (Unfortunately, Archipelago is a bit ambiguous about its terminology here:
    #  "filler" is an ItemClassification separate from "trap", but in a lot of its functions,
    #  Archipelago will use "filler" to just mean "an additional item created to fill out the itempool".
    #  "Filler" in this sense can technically have any ItemClassification,
    #  but most commonly ItemClassification.filler or ItemClassification.trap.
    #  Starting here, the word "filler" will be used to collectively refer to APQuest's Confetti Cannon and Math Trap,
    #  which are ItemClassification.filler and ItemClassification.trap respectively.)
    # Creating filler items works the same as any other item. But there is a question:
    # How many filler items do we actually need to create?
    # In regions.py, we created either six or seven locations depending on the "extra_starting_chest" option.
    # In this function, we have created five or six items depending on whether the "hammer" option is enabled.
    # We *could* have a really complicated if-else tree checking the options again, but there is a better way.
    # We can compare the size of our itempool so far to the number of locations in our world.

    # The length of our itempool is easy to determine, since we have it as a list.
    number_of_items = len(itempool)

    # The number of locations is also easy to determine, but we have to be careful.
    # Just calling len(world.get_locations()) would report an incorrect number, because of our *event locations*.
    # What we actually want is the number of *unfilled* locations. Luckily, there is a helper method for this:
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

    # Now, we just subtract the number of items from the number of locations to get the number of empty item slots.
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    # Finally, we create that many filler items and add them to the itempool.
    # To create our filler, we could just use world.create_item("Confetti Cannon").
    # But there is an alternative that works even better for most worlds, including APQuest.
    # As discussed above, our world must have a get_filler_item_name() function defined,
    # which must return the name of an infinitely repeatable filler item.
    # Defining this function enables the use of a helper function called world.create_filler().
    # You can just use this function directly to create as many filler items as you need to complete your itempool.
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    # But... is that the right option for your game? Let's explore that.
    # For some games, the concepts of "regular itempool filler" and "additionally created filler" are different.
    # These games might want / require specific amounts of specific filler items in their regular pool.
    # To achieve this, they will have to intentionally create the correct quantities using world.create_item().
    # They may still use world.create_filler() to fill up the rest of their itempool with "repeatable filler",
    # after creating their "specific quantity" filler and still having room left over.

    # But there are many other games which *only* have infinitely repeatable filler items.
    # They don't care about specific amounts of specific filler items, instead only caring about the proportions.
    # In this case, world.create_filler() can just be used for the entire filler itempool.
    # APQuest is one of these games:
    # Regardless of whether it's filler for the regular itempool or additional filler for item links / etc.,
    # we always just want a Confetti Cannon or a Math Trap depending on the "trap_chance" option.
    # We defined this behavior in our get_random_filler_item_name() function, which in world.py,
    # we'll bind to world.get_filler_item_name(). So, we can just use world.create_filler() for all of our filler.

    # Anyway. With our world's itempool finalized, we now need to submit it to the multiworld itempool.
    # This is how the generator actually knows about the existence of our items.
    world.multiworld.itempool += itempool

    # Sometimes, you might want the player to start with certain items already in their inventory.
    # These items are called "precollected items".
    # They will be sent as soon as they connect for the first time (depending on your client's item handling flag).
    # Players can add precollected items themselves via the generic "start_inventory" option.
    # If you want to add your own precollected items, you can do so via world.push_precollected().
    #if world.options.start_with_one_confetti_cannon:
        # We're adding a filler item, but you can also add progression items to the player's precollected inventory.
        #starting_confetti_cannon = world.create_item("Confetti Cannon")
        #world.push_precollected(starting_confetti_cannon)
