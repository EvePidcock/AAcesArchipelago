from __future__ import annotations

import dataclasses
import typing

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, True_, HasAll, HasAllCounts, HasAny, HasAnyCount, HasFromListUnique, Rule, TWorld, \
    False_
from typing import TYPE_CHECKING, override

from . import SpeciesUtils, Evolution, Tasks

if TYPE_CHECKING:
    from .world import EquilinoxWorld


def set_all_rules(world: EquilinoxWorld) -> None:
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_location_rules(world: EquilinoxWorld) -> None:
    set_evolution_rules(world)

    victory = world.get_location("Game finished")
    world.set_rule(victory, CanEvolveSpecies(SpeciesUtils.get_species_from_name("Dolphin")) & CanEvolveSpecies(SpeciesUtils.get_species_from_name("Sunflower")) & CanEvolveSpecies(SpeciesUtils.get_species_from_name("Camel")))
    return

def set_evolution_rules(world: EquilinoxWorld) -> None:
    evo_species = []
    for species in SpeciesUtils.all_species:
        if not species.is_base_species():
            evo_species.append(species)

    for species in evo_species:
        #if species.name == "Camel": raise RuntimeError("Camel")
        loc = world.get_location(f"Evolve {species.name}")
        world.set_rule(loc, CanEvolveSpecies(species))


def set_completion_condition(world: EquilinoxWorld) -> None:
    world.set_completion_rule(Has("Victory"))


@dataclasses.dataclass()
class CanEvolveSpecies(Rule['EquilinoxWorld'], game="Equilinox"):

    def __init__(self, species: SpeciesUtils.Species | None, depth: int = 1, species_to_ignore: list[SpeciesUtils.Species] = [], default: bool = True, options: typing.Iterable[OptionFilter] = (), filtered_resolution: bool = False):
        super().__init__(options = options, filtered_resolution = filtered_resolution)
        self.species = species
        self.depth = depth
        self.default = default
        self.species_to_ignore = species_to_ignore

    @override
    def _instantiate(self, world: 'EquilinoxWorld') -> Rule.Resolved:
        max_depth = 20
        space = ""
        for _ in range(self.depth):
            space += "\t"
        print(f"EQ:{space} Species {self.species.name} is at depth {self.depth}")

        if self.species is None:
            raise RuntimeError("none species")
        elif self.species.is_base_species():
            return Has(f"{self.species.name} Permit").resolve(world)
        else:
            if self.depth > max_depth:
                raise RuntimeError(f"Hit the max depth with {self.species.name}")
                if self.default:
                    return True_().resolve(world)
                else:
                    return False_().resolve(world)
            rule = True_()
            previous_species = self.species.get_previous_evolution()
            if previous_species is None:
                raise RuntimeError("none previous species")
                return rule.resolve(world)
            rule = rule & CanEvolveSpecies(previous_species, self.depth + 1, self.species_to_ignore, True)
            for req in self.species.evolution_requirements:
                rule = rule & req.get_rule(self.species, self.species_to_ignore + SpeciesUtils.get_all_priors(self.species) + [self.species], self.depth)
            return rule.resolve(world)