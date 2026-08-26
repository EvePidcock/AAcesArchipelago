from enum import Enum

from Species import Species, all_species, get_species_from_name


class RequirementType(Enum):
    COLOR = 1
    NEARBY_SPECIES = 2
    SATISFACTION = 3
    SIZE = 4
    BIOME = 5
    ALTITUDE = 6
    DIET = 7
    SPEED = 8

class EvolutionRequirement:
    def __init__(self, type: RequirementType):
        self.type = type



class ColorRequirement(EvolutionRequirement):
    def __init__(self, color: str):
        super().__init__(RequirementType.COLOR)
        self.color = color



def get_species_from_category(cat: str) -> list[Species]:
    return []

class NearbySpeciesRequirement(EvolutionRequirement):
    def __init__(self, species: str):
        super().__init__(RequirementType.NEARBY_SPECIES)
        self.species = species.split(";")

    def get_required_species(self) -> list[Species | None]:
        required : list[Species | None] = []
        for species in self.species:
            species = species.split(" (")[0]
            if get_species_from_name(species) is not None:
                required.append(get_species_from_name(species))
            else:
                required += get_species_from_name(species)
        return required



class SatisfactionRequirement(EvolutionRequirement):
    def __init__(self, satisfaction: int):
        super().__init__(RequirementType.SATISFACTION)
        self.satisfaction = satisfaction

class SizeRequirement(EvolutionRequirement):
    def __init__(self, size: int):
        super().__init__(RequirementType.SIZE)
        self.size = size

class BiomeRequirement(EvolutionRequirement):
    def __init__(self, biome: str):
        super().__init__(RequirementType.BIOME)
        self.biome = biome

class AltitudeRequirement(EvolutionRequirement):
    def __init__(self, altitude: str):
        super().__init__(RequirementType.ALTITUDE)
        self.altitude = altitude

class DietRequirement(EvolutionRequirement):
    def __init__(self, diet: str):
        super().__init__(RequirementType.DIET)
        self.diet = diet

class SpeedRequirement(EvolutionRequirement):
    def __init__(self, speed: int):
        super().__init__(RequirementType.SPEED)
        self.speed = speed