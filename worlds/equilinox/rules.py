from __future__ import annotations

import dataclasses
import typing

from BaseClasses import CollectionState
from rule_builder.field_resolvers import FieldResolver, FromOption
from rule_builder.options import OptionFilter
from rule_builder.rules import Has, True_, HasAll, HasAllCounts, HasAny, HasAnyCount, HasFromListUnique, Rule, TWorld, \
    False_
from typing import TYPE_CHECKING, override, Any

from . import SpeciesUtils, Evolution, Tasks
from .options import StartingDP

if TYPE_CHECKING:
    from .world import EquilinoxWorld


def set_all_rules(world: EquilinoxWorld) -> None:
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_location_rules(world: EquilinoxWorld) -> None:
    set_evolution_rules(world)
    set_task_rules(world)
    set_trait_rules(world)

    victory = world.get_location("Game finished")
    world.set_rule(victory, CanEvolveSpecies(SpeciesUtils.get_species_from_name("Dolphin")) & CanEvolveSpecies(SpeciesUtils.get_species_from_name("Sunflower")) & CanEvolveSpecies(SpeciesUtils.get_species_from_name("Camel")))
    return

def set_trait_rules(world: EquilinoxWorld) -> None:
    for species in SpeciesUtils.all_species:
        if species.name not in SpeciesUtils.get_species_from_category("Rocks/Stones"):
            sizeLoc1 = world.get_location(f"Big {species.name}! (Size 1.10)")
            sizeLoc2 = world.get_location(f"Small {species.name}! (Size 0.90)")
            world.set_rule(sizeLoc1, CanEvolveSpecies(species) & ReceivedEnoughDP(species.cost + 20000))
            world.set_rule(sizeLoc2, CanEvolveSpecies(species) & ReceivedEnoughDP(species.cost + 22000))

def set_evolution_rules(world: EquilinoxWorld) -> None:
    evo_species = []
    for species in SpeciesUtils.all_species:
        if not species.is_base_species():
            evo_species.append(species)

    for species in evo_species:
        #if species.name == "Camel": raise RuntimeError("Camel") # Debug
        loc = world.get_location(f"Evolve {species.name}")
        world.set_rule(loc, CanEvolveSpecies(species))


def set_task_rules(world: EquilinoxWorld) -> None:
    tasks = Tasks.all_tasks
    for task in tasks:
        task_loc = world.get_location(f"Complete Task '{task.name}'")
        rule = True_()
        for req_list in task.get_required_species():
            if len(req_list) == 0 or all(s is None for s in req_list):
                continue
            can_get_at_least_one_from_list = False_()
            for species in req_list:
                if species is None: continue
                can_get_at_least_one_from_list = can_get_at_least_one_from_list | ( CanEvolveSpecies(species) & ReceivedEnoughDP(species.cost * 3) )
            rule = rule & can_get_at_least_one_from_list

        if task.name == "Completionist":
            pass
        elif task.name == "Cashing In": # Task for earning 500 DP per minute. Logically, we have this require a few animals. Not super robust
            pass

        world.set_rule(task_loc, rule)

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
            rule = rule & CanEvolveSpecies(previous_species, self.depth + 1, self.species_to_ignore, True) & ReceivedEnoughDP(previous_species.cost * 2)
            for req in self.species.evolution_requirements:
                rule = rule & req.get_rule(self.species, self.species_to_ignore + SpeciesUtils.get_all_priors(self.species) + [self.species], self.depth)
            return rule.resolve(world)


@dataclasses.dataclass()
class ReceivedEnoughDP(Rule['EquilinoxWorld'], game="Equilinox"):

    def __init__(self, dp: int, options: typing.Iterable[OptionFilter] = (), filtered_resolution: bool = False):
        super().__init__(options=options, filtered_resolution=filtered_resolution)
        self.dp = dp

    @typing.override
    def _instantiate(self, world: 'EquilinoxWorld') -> Rule.Resolved:
        if self.dp <= 2500: return True_().resolve(world)
        return self.Resolved(self.dp, world.options.tasks_reward_dp.value == 1, player=world.player)

    class Resolved(Rule.Resolved):
        dp: int
        tasks_reward_dp: bool

        @typing.override
        def _evaluate(self, state: CollectionState) -> bool:
            padding = 0.8 # Leniency factor. Lower = more forgiving
            if self.tasks_reward_dp: padding = 1.0
            balance = 2500
            balance += state.count("100,000 dp", self.player) * 100000 * padding
            balance += state.count("75,000 dp", self.player)  *  75000 * padding
            balance += state.count("50,000 dp", self.player)  *  50000 * padding
            balance += state.count("25,000 dp", self.player)  *  25000 * padding
            balance += state.count("10,000 dp", self.player)  *  10000 * padding
            balance += state.count("7,500 dp", self.player)   *   7500 * padding
            balance += state.count("5,000 dp", self.player)   *   5000 * padding
            balance += state.count("2,500 dp", self.player)   *   2500 * padding
            balance += state.count("1,000 dp", self.player)   *   1000 * padding

            # Account for dp earn per minute by animals. There isn't a great way to do this cleanly,
            # so we just look at the base species. These factors are an attempt to account for
            # having later evolution stages (children) unlocked

            max_minutes_to_wait = 15
            children_factor = 2

            for animal in SpeciesUtils.get_species_from_category("Animals"):
                if not animal.is_base_species(): continue
                if state.has(f"{animal.name} Permit", self.player):
                    balance += animal.dp_earn * max_minutes_to_wait * children_factor

            return balance >= self.dp
