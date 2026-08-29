from __future__ import annotations
from abc import abstractmethod, ABC
from enum import Enum


from rule_builder.rules import Rule, True_, HasAny, HasAnyCount, False_
from .rules import CanEvolveSpecies
from . import world, SpeciesUtils
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .world import EquilinoxWorld


class RequirementType(Enum):
    COLOR = 1
    NEARBY_SPECIES = 2
    SATISFACTION = 3
    SIZE = 4
    BIOME = 5
    ALTITUDE = 6
    DIET = 7
    SPEED = 8

class EvolutionRequirement(ABC):
    def __init__(self, type: RequirementType):
        self.type = type

    @abstractmethod
    def get_rule(self, species: SpeciesUtils.Species, species_to_ignore: list[SpeciesUtils.Species], depth: int) -> Rule['EquilinoxWorld']:
        pass



class ColorRequirement(EvolutionRequirement):
    def __init__(self, color: str):
        super().__init__(RequirementType.COLOR)
        self.color = color

    def get_rule(self, species: SpeciesUtils.Species, species_to_ignore: list[SpeciesUtils.Species], depth: int) -> Rule['EquilinoxWorld']:
        return True_()


class NearbySpeciesRequirement(EvolutionRequirement):
    def __init__(self, species_str: str):
        super().__init__(RequirementType.NEARBY_SPECIES)
        self.species_str = species_str

    def get_required_species(self) -> list[list[SpeciesUtils.Species | None]]:
        return SpeciesUtils.get_required_species_from_string(self.species_str)

    def get_rule(self, species: SpeciesUtils.Species, species_to_ignore: list[SpeciesUtils.Species], depth: int) -> Rule['EquilinoxWorld']:
        rule = True_()

        print(f"Testing {species.name} (nearby):")
        for req_set in self.get_required_species():
            if len(req_set) == 0: continue
            print(f"\t{[s.name for s in req_set if s is not None]}")

        for req_set in self.get_required_species():
            if len(req_set) == 0: continue
            req_set = SpeciesUtils.remove_later_evo_stages(req_set)
            for s in SpeciesUtils.get_species_evo_tree(species):
                if s in req_set: req_set.remove(s)
            for s in species_to_ignore:
                if s in req_set: req_set.remove(s)
            checked_species = []
            req_set_rule = False_()
            if len(req_set) == 0 or all(s is None for s in req_set): req_set_rule = True_()
            for s in req_set:
                if s is None: raise RuntimeError("Got 'none' obj in nearby check")
                if s.name == species.name: continue
                if s in checked_species: continue

                checked_species.append(s)
                req_set_rule = req_set_rule | CanEvolveSpecies(s, depth + 1, species_to_ignore, default = False)
            rule = rule & req_set_rule

        return rule


class SatisfactionRequirement(EvolutionRequirement):
    def __init__(self, satisfaction: int):
        super().__init__(RequirementType.SATISFACTION)
        self.satisfaction = satisfaction

    def get_rule(self, species: SpeciesUtils.Species, species_to_ignore: list[SpeciesUtils.Species], depth: int) -> Rule['EquilinoxWorld']:
        return True_()

class SizeRequirement(EvolutionRequirement):
    def __init__(self, size: int):
        super().__init__(RequirementType.SIZE)
        self.size = size

    def get_rule(self, species: SpeciesUtils.Species, species_to_ignore: list[SpeciesUtils.Species], depth: int) -> Rule['EquilinoxWorld']:
        return True_()

class BiomeRequirement(EvolutionRequirement):
    def __init__(self, biome: str):
        super().__init__(RequirementType.BIOME)
        self.biome = biome

    def get_rule(self, species: SpeciesUtils.Species, species_to_ignore: list[SpeciesUtils.Species], depth: int) -> Rule['EquilinoxWorld']:
        return True_()

class AltitudeRequirement(EvolutionRequirement):
    def __init__(self, altitude: str):
        super().__init__(RequirementType.ALTITUDE)
        self.altitude = altitude

    def get_rule(self, species: SpeciesUtils.Species, species_to_ignore: list[SpeciesUtils.Species], depth: int) -> Rule['EquilinoxWorld']:
        return True_()

class DietRequirement(EvolutionRequirement):
    def __init__(self, diet: str):
        super().__init__(RequirementType.DIET)
        self.diet = diet

    def get_rule(self, species: SpeciesUtils.Species, species_to_ignore: list[SpeciesUtils.Species], depth: int) -> Rule['EquilinoxWorld']:
        required_species = SpeciesUtils.get_required_species_from_string(self.diet)
        rule = True_()

        print(f"Testing {species.name} (diet):")
        for req_set in required_species:
            if len(req_set) == 0: continue
            print(f"\t{[s.name for s in req_set if s is not None]}")

        for req_set in required_species:
            if len(req_set) == 0: continue
            req_set = SpeciesUtils.remove_later_evo_stages(req_set)
            for s in SpeciesUtils.get_species_evo_tree(species):
                if s in req_set: req_set.remove(s)
            for s in species_to_ignore:
                if s in req_set: req_set.remove(s)
            checked_species = []
            req_set_rule = False_()
            if len(req_set) == 0 or all(s is None for s in req_set): req_set_rule = True_()
            for s in req_set:
                if s is None: raise RuntimeError("Got 'none' obj in diet check")
                if s.name == species.name: continue
                if s in checked_species: continue

                checked_species.append(s)
                req_set_rule = req_set_rule | CanEvolveSpecies(s, depth + 1, species_to_ignore, default=False)
            rule = rule & req_set_rule
        return rule

class SpeedRequirement(EvolutionRequirement):
    def __init__(self, speed: int):
        super().__init__(RequirementType.SPEED)
        self.speed = speed

    def get_rule(self, species: SpeciesUtils.Species, species_to_ignore: list[SpeciesUtils.Species], depth: int) -> Rule['EquilinoxWorld']:
        return True_()