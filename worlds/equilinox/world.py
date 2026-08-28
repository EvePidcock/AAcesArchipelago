from collections.abc import Mapping
from typing import Any


# Imports of base Archipelago modules must be absolute.
from worlds.AutoWorld import World

# Imports of your world's files must be relative.
from . import items, locations, regions, rules, web_world, Tasks, SpeciesUtils
from . import options as equilinox_options  # rename due to a name conflict with World.options


class EquilinoxWorld(World):
    """
    Equilinox is
    """

    game = "Equilinox"


    web = web_world.EquilinoxWebWorld()

    options_dataclass = equilinox_options.EquilinoxOptions
    options: equilinox_options.EquilinoxOptions  # Common mistake: This has to be a colon (:), not an equals sign (=).

    SpeciesUtils.all_species = SpeciesUtils.get_species()

    items.set_item_names_to_id()
    Tasks.init_tasks()

    location_name_to_id = locations.get_loc_names_to_id_dict()
    item_name_to_id = items.ITEM_NAME_TO_ID

    origin_region_name = "Menu"

    def generate_early(self) -> None:
        self.push_precollected(self.create_item("Grass Tuft Permit"))
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
        return self.options.as_dict("test")

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> Any:
        return slot_data
