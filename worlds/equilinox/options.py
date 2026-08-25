from dataclasses import dataclass

from Options import OptionGroup, PerGameCommonOptions, Range, Toggle

class FlowerHunt(Toggle):
    """
    Require a certain number of "Flower" items to goal
    """
    display_name = "Flower Hunt"
    default = True

class FlowerItemsRequired(Range):
    """
    How many "Flower" items needed to goal.
    Does nothing if Flower Hunt is off.
    """
    display_name = "Required Flowers to Goal"
    range_start = 10
    range_end = 100
    default = 40


class FlowerItemsTotal(Range):
    """
    How many "Flower" items to put in the item pool.
    Does nothing if Flower Hunt is off.
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
    If on, you will not be logically required to play
    a card with a black or brown ability you can not activate
    """
    display_name = "Kinder Card Logic"
    default = True

class ProgressionCardCount(Range):
    """
    The maximum number of "Play card..." locations that can contain progression items.
    Smaller numbers increase the chances that event cards will hold progression items.
    """
    display_name = "Card Play Prog Item Cap"
    range_start = 0
    range_end = 300
    default = 100



@dataclass
class EquilinoxOptions(PerGameCommonOptions):
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
    allowed_progression_cards: ProgressionCardCount


option_groups = [
    OptionGroup(
        "Goal Options",
        [FlowerHunt, FlowerItemsRequired, FlowerItemsTotal]
    ),
    OptionGroup(
        "Gameplay Options",
        [StartingIslandsCount, StartingClimatesCount, StartWithSproutStorage, StartingLeaf, StartingSeed, StartingPersonalEcosystem, KinderCardLogic, ProgressionCardCount]
    )
]

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
        "kinder_card_logic": True,
        "allowed_progression_cards": 50
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
        "kinder_card_logic": False,
        "allowed_progression_cards": 300
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
        "kinder_card_logic": True,
        "allowed_progression_cards": 50
    }
}
