from dataclasses import dataclass

from Options import OptionGroup, PerGameCommonOptions, Range, Toggle

class Test(Toggle):
    """
    Require a certain number of "Flower" items to goal
    """
    display_name = "Test"
    default = True

@dataclass
class EquilinoxOptions(PerGameCommonOptions):
    test: Test


option_groups = [
    OptionGroup(
        "Gameplay Options",
        [Test]
    )
]

option_presets = {
    "Default": {
        "test": True
    }
}
