from collections.abc import Mapping
from typing import Any

# Imports of base Archipelago modules must be absolute.
from worlds.AutoWorld import World

# Imports of your world's files must be relative.
from . import items, locations, regions, rules, web_world
from . import options as earth_options  # rename due to a name conflict with World.options


class EarthWorld(World):
    """
    Earth is a tableau-building, engine-building board game for 1-6 players. This implementation is of the solo game mode
    """

    game = "Earth"


    web = web_world.EarthWebWorld()

    starting_islands = []
    starting_climates = []

    options_dataclass = earth_options.EarthOptions
    options: earth_options.EarthOptions  # Common mistake: This has to be a colon (:), not an equals sign (=).

    location_name_to_id = locations.get_loc_names_to_id_dict()
    item_name_to_id = items.ITEM_NAME_TO_ID

    origin_region_name = "Main"

    def generate_early(self) -> None:
        island_unlocks = ["Island Unlock: Fogo / Whakaari",
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
                    "Island Unlock: Java Island / Madagascar Island"]
        climate_unlocks = ["Climate Unlock: Hemiboreal / Tropical Savanna",
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
                    "Climate Unlock: Cold Winter Continental / Temperate Hot Summer"]

        starting_islands_count = self.options.starting_islands_count.value
        starting_climates_count = self.options.starting_climates_count.value

        self.starting_islands = self.random.sample(island_unlocks, starting_islands_count)
        self.starting_climates = self.random.sample(climate_unlocks, starting_climates_count)

        for island in self.starting_islands:
            self.push_precollected(self.create_item(island))

        for climate in self.starting_climates:
            self.push_precollected(self.create_item(climate))

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.EarthItem:
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
