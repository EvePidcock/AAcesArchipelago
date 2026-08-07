from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

# In this file, we define the options the player can pick.
# The most common types of options are Toggle, Range and Choice.

# Options will be in the game's template yaml.
# They will be represented by checkboxes, sliders etc. on the game's options page on the website.
# (Note: Options can also be made invisible from either of these places by overriding Option.visibility.
#  APQuest doesn't have an example of this, but this can be used for secret / hidden / advanced options.)

# For further reading on options, you can also read the Options API Document:
# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/options%20api.md


# The first type of Option we'll discuss is the Toggle.
# A toggle is an option that can either be on or off. This will be represented by a checkbox on the website.
# The default for a toggle is "off".
# If you want a toggle to be on by default, you can use the "DefaultOnToggle" class instead of the "Toggle" class.
class FlowerHunt(Toggle):
    """
    Require a certain number of "Flower" items to goal
    """
    display_name = "Flower Hunt"
    default = True


class FlowerItemsRequired(Range):
    """
    How many "Flower" items needed to goal. Does nothing if Flower Hunt is off.
    """
    display_name = "Required Flowers to Goal"
    range_start = 10
    range_end = 100
    default = 40


class FlowerItemsTotal(Range):
    """
    How many "Flower" items to put in the item pool. Does nothing if Flower Hunt is off.
    """
    display_name = "Total Flowers"
    range_start = 10
    range_end = 120
    default = 50


class StartingIslandsCount(Range):
    """
    How many island *cards* to start with (min 1)
    """
    display_name = "Starting Islands Count"
    range_start = 1
    range_end = 12
    default = 2


class StartingClimatesCount(Range):
    """
    How many climate *cards* to start with (min 0)
    """
    display_name = "Starting Climates Count"
    range_start = 0
    range_end = 12
    default = 2

class StartWithSproutStorage(Toggle):
    """
    Should the Sprout Storage be unlocked initially
    """
    display_name = "Starting Sprout Storage"
    default = False

class StartingLeaf(Toggle):
    """
    Should you start with a leaf
    """
    display_name = "Starting Leaf"
    default = True

class StartingSeed(Toggle):
    """
    Should you start with a seed
    """
    display_name = "Starting Seed"
    default = False

class StartingPersonalEcosystem(Toggle):
    """
    Should you start with the ability to choose a personal ecosystem
    """
    display_name = "Starting Personal Ecosystem"
    default = False

class KinderCardLogic(Toggle):
    """
    If on, you will not be logically required to play a card with a black or brown ability you can not activate
    """
    display_name = "Kinder Card Logic"
    default = True


# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName".
@dataclass
class EarthOptions(PerGameCommonOptions):
    flower_hunt: FlowerHunt
    flowers_required: FlowerItemsRequired
    flowers_total: FlowerItemsTotal
    starting_islands_count: StartingIslandsCount
    starting_climates_count: StartingClimatesCount
    starting_sprout_storage: StartWithSproutStorage
    starting_leaf: StartingLeaf
    starting_seed: StartingSeed
    starting_personal_ecosystem: StartingPersonalEcosystem
    kinder_card_logic: KinderCardLogic


# If we want to group our options by similar type, we can do so as well. This looks nice on the website.
option_groups = [
    OptionGroup(
        "Goal Options",
        [FlowerHunt, FlowerItemsRequired, FlowerItemsTotal]
    ),
    OptionGroup(
        "Gameplay Options",
        [StartingIslandsCount, StartingClimatesCount, StartWithSproutStorage, StartingLeaf, StartingSeed, StartingPersonalEcosystem, KinderCardLogic]
    )
]

# Finally, we can define some option presets if we want the player to be able to quickly choose a specific "mode".
option_presets = {
    "Default": {
        "flower_hunt": True,
        "flowers_required": 40,
        "flowers_total": 50,
        "starting_islands_count": 2,
        "starting_climates_count": 2,
        "starting_sprout_storage": False,
        "starting_leaf": True,
        "starting_seed": False,
        "starting_personal_ecosystem": False,
        "kinder_card_logic": True
    },
    "Pain": {
        "flower_hunt": True,
        "flowers_required": 80,
        "flowers_total": 100,
        "starting_islands_count": 1,
        "starting_climates_count": 0,
        "starting_sprout_storage": False,
        "starting_leaf": False,
        "starting_seed": False,
        "starting_personal_ecosystem": False,
        "kinder_card_logic": False
    },
    "Easier Start": {
        "flower_hunt": True,
        "flowers_required": 35,
        "flowers_total": 50,
        "starting_islands_count": 4,
        "starting_climates_count": 4,
        "starting_sprout_storage": True,
        "starting_leaf": True,
        "starting_seed": True,
        "starting_personal_ecosystem": True,
        "kinder_card_logic": True
    }
}
