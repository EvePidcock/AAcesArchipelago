from __future__ import annotations
from abc import abstractmethod, ABC
from enum import Enum

from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
from rule_builder.rules import Rule, True_, HasAny, HasAnyCount, False_
from .rules import CanEvolveSpecies, ReceivedEnoughDP
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
    
    @abstractmethod
    def explain(self, world: EquilinoxWorld, species: SpeciesUtils.Species, state: CollectionState) -> list[JSONMessagePart]:
        pass



class ColorRequirement(EvolutionRequirement):
    def __init__(self, color: str):
        super().__init__(RequirementType.COLOR)
        self.color = color

    def get_rule(self, species: SpeciesUtils.Species, species_to_ignore: list[SpeciesUtils.Species], depth: int) -> Rule['EquilinoxWorld']:
        return True_()

    def explain(self, world: EquilinoxWorld, species: SpeciesUtils.Species, state: CollectionState) -> list[JSONMessagePart]:
        messages: list[JSONMessagePart] = [{"type": "text", "text": "\n    Color Requirement:"}]
        messages.append({"type": "color", "color": "green", "text": f"\n        {self.color}"})
        return messages


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
                req_set_rule = req_set_rule | (CanEvolveSpecies(s, depth + 1, species_to_ignore, default = False) & ReceivedEnoughDP(s.cost))
            rule = rule & req_set_rule

        return rule
    
    def explain(self, world: EquilinoxWorld, species: SpeciesUtils.Species, state: CollectionState) -> list[JSONMessagePart]:
        messages: list[JSONMessagePart] = [{"type": "text", "text": "\n    Nearby Species Requirement(s):"}]

        categories = self.species_str.split(";")
        species_lists = self.get_required_species()

        for cat_index in range(len(categories)):
            if len(species_lists[cat_index]) == 0: continue
            if len(species_lists[cat_index]) == 1:
                species = species_lists[cat_index][0]
                if species.is_base_species():
                    has_prereq = state.has(f"{species.name} Permit", world.player)
                    messages.append({"type": "color", "color": "green" if has_prereq else "salmon", "text": f"\n        {species.name}"})
                    if not has_prereq: messages.append({"type": "text", "text": f" (missing unlock permit)"})
                else:
                    has_prereq = world.get_location(f"Evolve {species.name}").can_reach(state)
                    messages.append({"type": "color", "color": "green" if has_prereq else "salmon", "text": f"\n        {species.name}"})
                    if not has_prereq: messages.append({"type": "text", "text": f" (evolution not in logic)"})
            else:
                has_prereq = False
                for species in species_lists[cat_index]:
                    if species.is_base_species():
                        has_prereq |= state.has(f"{species.name} Permit", world.player)
                    else:
                        has_prereq |= world.get_location(f"Evolve {species.name}").can_reach(state)
                messages.append({"type": "color", "color": "green" if has_prereq else "salmon", "text": f"\n        {categories[cat_index]}"})

        return messages


class SatisfactionRequirement(EvolutionRequirement):
    def __init__(self, satisfaction: int):
        super().__init__(RequirementType.SATISFACTION)
        self.satisfaction = satisfaction

    def get_rule(self, species: SpeciesUtils.Species, species_to_ignore: list[SpeciesUtils.Species], depth: int) -> Rule['EquilinoxWorld']:
        return True_()
    
    def explain(self, world: EquilinoxWorld, species: SpeciesUtils.Species, state: CollectionState) -> list[JSONMessagePart]:
        messages: list[JSONMessagePart] = [{"type": "text", "text": "\n    Satisfaction Requirement:"}]
        messages.append({"type": "color", "color": "green", "text": f"\n        {self.satisfaction}"})
        return messages

class SizeRequirement(EvolutionRequirement):
    def __init__(self, size: int):
        super().__init__(RequirementType.SIZE)
        self.size = size

    def get_rule(self, species: SpeciesUtils.Species, species_to_ignore: list[SpeciesUtils.Species], depth: int) -> Rule['EquilinoxWorld']:
        return True_()
    
    def explain(self, world: EquilinoxWorld, species: SpeciesUtils.Species, state: CollectionState) -> list[JSONMessagePart]:
        messages: list[JSONMessagePart] = [{"type": "text", "text": "\n    Size Requirement:"}]
        messages.append({"type": "color", "color": "green", "text": f"\n        {self.size}"})
        return messages

class BiomeRequirement(EvolutionRequirement):
    def __init__(self, biome: str):
        super().__init__(RequirementType.BIOME)
        self.biome = biome

    def get_rule(self, species: SpeciesUtils.Species, species_to_ignore: list[SpeciesUtils.Species], depth: int) -> Rule['EquilinoxWorld']:
        return True_()
    
    def explain(self, world: EquilinoxWorld, species: SpeciesUtils.Species, state: CollectionState) -> list[JSONMessagePart]:
        messages: list[JSONMessagePart] = [{"type": "text", "text": "\n    Biome Requirement:"}]
        biome_reqs = self.biome.split(";")
        messages.append({"type": "color", "color": "green", "text": f"\n        {biome_reqs[0]} ({biome_reqs[1]}%)"})
        return messages

class AltitudeRequirement(EvolutionRequirement):
    def __init__(self, altitude: str):
        super().__init__(RequirementType.ALTITUDE)
        self.altitude = altitude

    def get_rule(self, species: SpeciesUtils.Species, species_to_ignore: list[SpeciesUtils.Species], depth: int) -> Rule['EquilinoxWorld']:
        return True_()
    
    def explain(self, world: EquilinoxWorld, species: SpeciesUtils.Species, state: CollectionState) -> list[JSONMessagePart]:
        messages: list[JSONMessagePart] = [{"type": "text", "text": "\n    Altitude Requirement:"}]
        messages.append({"type": "color", "color": "green", "text": f"\n        {self.altitude}"})
        return messages

class DietRequirement(EvolutionRequirement):
    def __init__(self, diet: str):
        super().__init__(RequirementType.DIET)
        self.diet = diet

    def get_rule(self, species: SpeciesUtils.Species, species_to_ignore: list[SpeciesUtils.Species], depth: int) -> Rule['EquilinoxWorld']:
        required_species = SpeciesUtils.get_required_species_from_string(self.diet)

        required_species = required_species[0]

        if required_species is None: raise RuntimeError(f"Diet requirement none for {species.name}")
        if len(required_species) == 0: raise RuntimeError(f"Diet requirement none for {species.name}")

        if len(required_species) > 1:
            req_set = SpeciesUtils.remove_later_evo_stages(required_species)
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
                req_set_rule = req_set_rule | (CanEvolveSpecies(s, depth + 1, species_to_ignore, default=False) & ReceivedEnoughDP(s.cost))
            return req_set_rule
        else:
            return CanEvolveSpecies(required_species[0]) & ReceivedEnoughDP(required_species[0].cost * 2)
    
    def explain(self, world: EquilinoxWorld, species: SpeciesUtils.Species, state: CollectionState) -> list[JSONMessagePart]:
        messages: list[JSONMessagePart] = [{"type": "text", "text": "\n    Diet Requirement:"}]

        required_species = SpeciesUtils.get_required_species_from_string(self.diet)

        required_species = required_species[0]

        if required_species is None: raise RuntimeError(f"Diet requirement none for {species.name}")
        if len(required_species) == 0: raise RuntimeError(f"Diet requirement none for {species.name}")

        if len(required_species) == 1:
            species = required_species[0]
            if species.is_base_species():
                has_prereq = state.has(f"{species.name} Permit", world.player)
                messages.append(
                    {"type": "color", "color": "green" if has_prereq else "salmon", "text": f"\n        {species.name}"})
                if not has_prereq: messages.append({"type": "text", "text": f" (missing unlock permit)"})
            else:
                has_prereq = world.get_location(f"Evolve {species.name}").can_reach(state)
                messages.append(
                    {"type": "color", "color": "green" if has_prereq else "salmon", "text": f"\n        {species.name}"})
                if not has_prereq: messages.append({"type": "text", "text": f" (evolution not in logic)"})
        else:
            has_prereq = False
            for species in required_species:
                if species.is_base_species():
                    has_prereq |= state.has(f"{species.name} Permit", world.player)
                else:
                    has_prereq |= world.get_location(f"Evolve {species.name}").can_reach(state)
            messages.append(
                {"type": "color", "color": "green" if has_prereq else "salmon", "text": f"\n\t{self.diet}"})

        return messages

class SpeedRequirement(EvolutionRequirement):
    def __init__(self, speed: int):
        super().__init__(RequirementType.SPEED)
        self.speed = speed

    def get_rule(self, species: SpeciesUtils.Species, species_to_ignore: list[SpeciesUtils.Species], depth: int) -> Rule['EquilinoxWorld']:
        return True_()
    
    def explain(self, world: EquilinoxWorld, species: SpeciesUtils.Species, state: CollectionState) -> list[JSONMessagePart]:
        messages: list[JSONMessagePart] = [{"type": "text", "text": "\n    Speed Requirement:"}]
        messages.append({"type": "color", "color": "green", "text": f"\n        {self.speed}"})
        return messages