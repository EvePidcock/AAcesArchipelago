from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location, Region, Item

from . import items, SpeciesUtils, Tasks, Evolution

if TYPE_CHECKING:
    from .world import EquilinoxWorld

class EquilinoxLocation(Location):
    game = "Equilinox"

    def __init__(self, player, name, id: int, region: Region):
        super().__init__(player, name, id, region)

def get_loc_names_to_id_dict() -> dict[str, int]:
    loc_name_to_id = {}

    all_species = SpeciesUtils.all_species
    all_tasks = Tasks.all_tasks

    for task in all_tasks:
        loc_name_to_id[f"Complete Task '{task.name}'"] = task.id + 10000

    for species in all_species:

        if species.name not in SpeciesUtils.get_species_from_category("Rocks/Stones"):
            # TODO: Make this an option
            # Size checks: 31XYYYZZZ
            locId = 310
            if not species.is_plant: # X = 1 if animal else 0
                locId += 1
            locId *= 1000
            locId += species.id # YYY = species id
            locId *= 1000
            locId += 110 # ZZZ = size (110 <=> 1.10)

            loc_name_to_id[f"Big {species.name}! (Size 1.10)"] = locId

            locId -= 20

            loc_name_to_id[f"Small {species.name}! (Size 0.90)"] = locId

        if not species.is_base_species():
            id = species.id
            loc_name = f"Evolve {species.name}"
            if species.is_plant:
                id += 20000
            else:
                id += 21000
            loc_name_to_id[loc_name] = id



    return loc_name_to_id

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: get_loc_names_to_id_dict()[location_name] for location_name in location_names}

def create_all_locations(world: EquilinoxWorld) -> None:
    create_regular_locations(world)
    create_events(world)

def create_regular_locations(world: EquilinoxWorld) -> None:

    menu = world.get_region("Menu")

    menu.add_locations(get_loc_names_to_id_dict(), EquilinoxLocation)


def create_events(world: EquilinoxWorld) -> None:
    world.get_region("Menu").add_event(
        "Game finished", "Victory", location_type=EquilinoxLocation, item_type=items.EquilinoxItem
    )