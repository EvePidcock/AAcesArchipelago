from dataclasses import dataclass

from Options import OptionGroup, PerGameCommonOptions, Range, Toggle

class TasksRewardDP(Toggle):
    """
    Should tasks reward the normal DP amount upon completion.
    If off, some filler DP items are replaced with larger
    sums of DP to replace the missing task rewards.
    """
    display_name = "Tasks Reward DP"
    default = True

class StartingDP(Range):
    """
    Starting DP Balance. The vanilla value is 2500.
    This is not exact; you will start with a balance *near* the selected value.
    """
    display_name = "Starting DP Balance"
    range_start = 2500
    range_end = 100000
    default = 5000

class DPInItempool(Range):
    """
    How much DP should be in the itempool? Note, currently the only filler
    item is small amounts of DP, so there will be more than just this much
    in the item pool. This option allows you to force the addition of larger
    DP items to the pool. If 'Tasks Reward DP' is off, some larger DP amounts
    will have already been added. We recommend at least some additional DP,
    since you may receive expensive Species before having a lot of DP earn per minute.
    """
    display_name = "Additional DP in Itempool"
    range_start = 0
    range_end = 500000
    default = 150000

@dataclass
class EquilinoxOptions(PerGameCommonOptions):
    tasks_reward_dp: TasksRewardDP
    starting_dp: StartingDP
    itempool_dp: DPInItempool

option_groups = [
    OptionGroup(
        "Gameplay Options",
        [TasksRewardDP, StartingDP, DPInItempool],
    )
]

option_presets = {
    "Default": {
        "tasks_reward_dp": True,
        "starting_dp": 5000,
        "itempool_dp": 150000
    }
}
