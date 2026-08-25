from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location, Region, Item

from . import items

if TYPE_CHECKING:
    from .world import EquilinoxWorld

class EquilinoxLocation(Location):
    game = "Equilinox"

    def __init__(self, player, name, id: int, region: Region):
        super().__init__(player, name, id, region)

def get_loc_names_to_id_dict() -> dict[str, int]:
    loc_name_to_id = {


    }
    return loc_name_to_id

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: get_loc_names_to_id_dict()[location_name] for location_name in location_names}

def create_all_locations(world: EquilinoxWorld) -> None:
    create_regular_locations(world)
    create_events(world)

def create_regular_locations(world: EquilinoxWorld) -> None:

    menu = world.get_region("Menu")


    locs = []


    menu.locations += locs


def create_events(world: EquilinoxWorld) -> None:
    world.get_region("Events").add_event(
        "Game finished", "Victory", location_type=EquilinoxLocation, item_type=items.EquilinoxItem
    )