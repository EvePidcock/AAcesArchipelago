from __future__ import annotations
from abc import abstractmethod, ABC
from enum import Enum

from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
from . import SpeciesUtils, rules
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
    def explain(self, world: EquilinoxWorld, species: SpeciesUtils.Species, state: CollectionState) -> list[JSONMessagePart]:
        pass



class ColorRequirement(EvolutionRequirement):
    def __init__(self, color: str):
        super().__init__(RequirementType.COLOR)
        self.color = color

    def explain(self, world: EquilinoxWorld, species: SpeciesUtils.Species, state: CollectionState) -> list[JSONMessagePart]:
        messages: list[JSONMessagePart] = [{"type": "text", "text": "\n    Color Requirement:"}]
        messages.append({"type": "color", "color": "green", "text": f"\n        {self.color}"})
        return messages


class NearbySpeciesRequirement(EvolutionRequirement):
    def __init__(self, species_str: str):
        super().__init__(RequirementType.NEARBY_SPECIES)
        self.species_str = species_str

    def get_required_species(self) -> list[set[SpeciesUtils.Species | None]]:
        return SpeciesUtils.get_required_species_from_string(self.species_str)
    
    def explain(self, world: EquilinoxWorld, species: SpeciesUtils.Species, state: CollectionState) -> list[JSONMessagePart]:
        messages: list[JSONMessagePart] = [{"type": "text", "text": "\n    Nearby Species Requirement(s):"}]

        categories = self.species_str.split(";")
        species_lists = self.get_required_species()

        for cat_index in range(len(categories)):
            if len(species_lists[cat_index]) == 0: continue
            if len(species_lists[cat_index]) == 1:
                species = species_lists[cat_index].pop()
                assert species is not None
                has_prereq = True #rules._can_evolve_species(world, species, state)
                can_afford = rules._can_afford_dp(world, species.cost, state)
                messages.append({"type": "color", "color": "green" if has_prereq and can_afford else "salmon",
                                 "text": f"\n        {species.name}"})
                if not has_prereq:
                    messages.append({"type": "text", "text": f" ({'missing unlock permit' if species.is_base_species() else 'evolution not in logic'})"})
                elif not can_afford:
                    messages.append({"type": "text", "text": f" ({'unlocked' if species.is_base_species() else 'evolution in logic'}, but cost not in logic)"})
            else:
                has_prereq = False
                for species in species_lists[cat_index]:
                    if species is None: continue
                    has_prereq |= True #rules._can_evolve_species(world, species, state) and rules._can_afford_dp(world, species.cost, state)
                messages.append({"type": "color", "color": "green" if has_prereq else "salmon", "text": f"\n        {categories[cat_index]}"})

        return messages


class SatisfactionRequirement(EvolutionRequirement):
    def __init__(self, satisfaction: int):
        super().__init__(RequirementType.SATISFACTION)
        self.satisfaction = satisfaction
    
    def explain(self, world: EquilinoxWorld, species: SpeciesUtils.Species, state: CollectionState) -> list[JSONMessagePart]:
        messages: list[JSONMessagePart] = [{"type": "text", "text": "\n    Satisfaction Requirement:"}]
        messages.append({"type": "color", "color": "green", "text": f"\n        {self.satisfaction}"})
        return messages

class SizeRequirement(EvolutionRequirement):
    def __init__(self, size: int):
        super().__init__(RequirementType.SIZE)
        self.size = size
    
    def explain(self, world: EquilinoxWorld, species: SpeciesUtils.Species, state: CollectionState) -> list[JSONMessagePart]:
        messages: list[JSONMessagePart] = [{"type": "text", "text": "\n    Size Requirement:"}]
        messages.append({"type": "color", "color": "green", "text": f"\n        {self.size}"})
        return messages

class BiomeRequirement(EvolutionRequirement):
    def __init__(self, biome: str):
        super().__init__(RequirementType.BIOME)
        self.biome = biome.split(";")[0]
        self.amt: int = int(biome.split(";")[1])
    
    def explain(self, world: EquilinoxWorld, species: SpeciesUtils.Species, state: CollectionState) -> list[JSONMessagePart]:
        messages: list[JSONMessagePart] = [{"type": "text", "text": "\n    Biome Requirement:"}]

        can_attain = True #rules._can_access_biome(self.biome, self.amt, rules.get_accessible_species(world, state))
        messages.append({"type": "color", "color": "green" if can_attain else "salmon", "text": f"\n        {self.biome} ({self.amt}%)"})
        return messages

class AltitudeRequirement(EvolutionRequirement):
    def __init__(self, altitude: str):
        super().__init__(RequirementType.ALTITUDE)
        self.altitude = altitude
    
    def explain(self, world: EquilinoxWorld, species: SpeciesUtils.Species, state: CollectionState) -> list[JSONMessagePart]:
        messages: list[JSONMessagePart] = [{"type": "text", "text": "\n    Altitude Requirement:"}]
        messages.append({"type": "color", "color": "green", "text": f"\n        {self.altitude}"})
        return messages

class DietRequirement(EvolutionRequirement):
    def __init__(self, diet: str):
        super().__init__(RequirementType.DIET)
        self.diet = diet

    def get_required_species(self) -> list[set[SpeciesUtils.Species | None]]:
        return SpeciesUtils.get_required_species_from_string(self.diet)
    
    def explain(self, world: EquilinoxWorld, species: SpeciesUtils.Species, state: CollectionState) -> list[JSONMessagePart]:
        messages: list[JSONMessagePart] = [{"type": "text", "text": "\n    Diet Requirement:"}]

        required_species = SpeciesUtils.get_required_species_from_string(self.diet)

        required_species = required_species[0]

        if required_species is None: raise RuntimeError(f"Diet requirement none for {species.name}")
        if len(required_species) == 0: raise RuntimeError(f"Diet requirement none for {species.name}")

        if len(required_species) == 1:
            species = required_species.pop()
            assert species is not None
            has_prereq = True #rules._can_evolve_species(world, species, state)
            can_afford = rules._can_afford_dp(world, species.cost, state)
            messages.append({"type": "color", "color": "green" if has_prereq and can_afford else "salmon",
                             "text": f"\n        {species.name}"})
            if not has_prereq:
                messages.append({"type": "text",
                                 "text": f" ({'missing unlock permit' if species.is_base_species() else 'evolution not in logic'})"})
            elif not can_afford:
                messages.append({"type": "text",
                                 "text": f" ({'unlocked' if species.is_base_species() else 'evolution in logic'}, but cost not in logic)"})
        else:
            has_prereq = False
            for species in required_species:
                has_prereq |= True #rules._can_evolve_species(world, species, state) and rules._can_afford_dp(world, species.cost, state)
            messages.append(
                {"type": "color", "color": "green" if has_prereq else "salmon", "text": f"\n\t{self.diet}"})

        return messages

class SpeedRequirement(EvolutionRequirement):
    def __init__(self, speed: int):
        super().__init__(RequirementType.SPEED)
        self.speed = speed
    
    def explain(self, world: EquilinoxWorld, species: SpeciesUtils.Species, state: CollectionState) -> list[JSONMessagePart]:
        messages: list[JSONMessagePart] = [{"type": "text", "text": "\n    Speed Requirement:"}]
        messages.append({"type": "color", "color": "green", "text": f"\n        {self.speed}"})
        return messages