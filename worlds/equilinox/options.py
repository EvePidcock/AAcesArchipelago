from dataclasses import dataclass

from Options import OptionGroup, PerGameCommonOptions, Range, Toggle

class MoneySanity(Toggle):
    """
    Shuffle Task DP rewards into the item pool
    """
    display_name = "Money Sanity"
    default = False

@dataclass
class EquilinoxOptions(PerGameCommonOptions):
    money_sanity: MoneySanity


option_groups = [
    OptionGroup(
        "Gameplay Options",
        [MoneySanity],
    )
]

option_presets = {
    "Default": {
        "money_sanity": False
    }
}
