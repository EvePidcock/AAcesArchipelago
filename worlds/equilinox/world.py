from collections.abc import Mapping
from typing import Any

# Imports of base Archipelago modules must be absolute.
from worlds.AutoWorld import World

# Imports of your world's files must be relative.
from . import items, locations, regions, rules, web_world
from . import options as earth_options  # rename due to a name conflict with World.options


class EquilinoxWorld(World):
    """
    Equilinox is
    """

    game = "Equilinox"


    web = web_world.EquilinoxWebWorld()

    starting_islands = []
    starting_climates = []

    options_dataclass = earth_options.EquilinoxOptions
    options: earth_options.EquilinoxOptions  # Common mistake: This has to be a colon (:), not an equals sign (=).

    location_name_to_id = locations.get_loc_names_to_id_dict()
    item_name_to_id = items.ITEM_NAME_TO_ID

    origin_region_name = "Menu"

    def generate_early(self) -> None:
        return

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.EquilinoxItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        slot_data = {"starting_islands": self.starting_islands, "starting_climates": self.starting_climates}
        slot_data.update(self.options.as_dict(
            "flower_hunt", "flowers_required", "flowers_total", "starting_islands_count", "starting_climates_count", "kinder_card_logic", "allowed_progression_cards"
        ))
        return slot_data

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> Any:
        return slot_data
