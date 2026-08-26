from __future__ import annotations

import json
import pkgutil

from Evolution import EvolutionRequirement, ColorRequirement, NearbySpeciesRequirement, SatisfactionRequirement, \
    SizeRequirement, BiomeRequirement, AltitudeRequirement, DietRequirement, SpeedRequirement

def get_species_from_name(name: str) -> Species | None:
    for species in all_species:
        if species.name == name:
            return species
    return None

class Species:
    def __init__(self,
                 is_plant: bool,
                 name: str,
                 evolution_stage: int,
                 previous_evolution: str,
                 evolution_requirements: list[EvolutionRequirement],
                 id: int):
        self.is_plant = is_plant
        self.name = name
        self.evolution_stage = evolution_stage
        self.previous_evolution = previous_evolution
        self.evolution_requirements = evolution_requirements
        self.id = id

    def get_previous_evolution(self) -> Species | None:
        return get_species_from_name(self.previous_evolution)

    def is_base_species(self) -> bool:
        return self.evolution_stage == 1


def get_evolution_reqs_from_json(e_obj) -> list[EvolutionRequirement]:
    reqs = []

    if e_obj["color"] != "":
        reqs.append(ColorRequirement(e_obj["color"]))

    if e_obj["nearby_species"] != "":
        reqs.append(NearbySpeciesRequirement(e_obj["nearby_species"]))

    if e_obj["satisfaction"] != 0:
        reqs.append(SatisfactionRequirement(e_obj["satisfaction"]))

    if e_obj["size"] != 0:
        reqs.append(SizeRequirement(e_obj["size"]))

    if e_obj["biome"] != "":
        reqs.append(BiomeRequirement(e_obj["biome"]))

    if e_obj["altitude"] != "":
        reqs.append(AltitudeRequirement(e_obj["altitude"]))

    if e_obj.keys().contains("diet"):
        if e_obj["diet"] != "":
            reqs.append(DietRequirement(e_obj["diet"]))
        if e_obj["speed"] != 0:
            reqs.append(SpeedRequirement(e_obj["speed"]))

    return reqs

def plant_object_decoder(p_obj):
    return Species(True, p_obj["name"], p_obj["evolution_stage"], p_obj["previous_evolution"], get_evolution_reqs_from_json(p_obj["evolution_requirements"]), p_obj["id"])

def animal_object_decoder(a_obj):
    return Species(False, a_obj["name"], a_obj["evolution_stage"], a_obj["previous_evolution"], get_evolution_reqs_from_json(a_obj["evolution_requirements"]), a_obj["id"])

def get_species() -> list[Species]:
    return get_plants() + get_animals()

def get_plants() -> list[Species]:
    plants_raw_data = pkgutil.get_data(
        __name__, "data/plants.json")
    if plants_raw_data:
        data = json.loads(
            plants_raw_data, object_hook=plant_object_decoder)
        eco_list: list[Species] = list(data)
        return eco_list
    empty_list: list[Species] = []
    return empty_list

def get_animals() -> list[Species]:
    animals_raw_data = pkgutil.get_data(
        __name__, "data/animals.json")
    if animals_raw_data:
        data = json.loads(
            animals_raw_data, object_hook=animal_object_decoder)
        eco_list: list[Species] = list(data)
        return eco_list
    empty_list: list[Species] = []
    return empty_list

all_species : list[Species] = get_species()