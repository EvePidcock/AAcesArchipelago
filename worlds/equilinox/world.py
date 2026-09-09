from collections.abc import Mapping
from typing import Any

from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
# Imports of base Archipelago modules must be absolute.
from worlds.AutoWorld import World
from Utils import get_fuzzy_results, get_intended_text
# Imports of your world's files must be relative.
from . import items, locations, regions, rules, web_world, Tasks, SpeciesUtils
from . import options as equilinox_options  # rename due to a name conflict with World.options


class EquilinoxWorld(World):
    """
    Equilinox is
    """

    game = "Equilinox"


    web = web_world.EquilinoxWebWorld()

    options_dataclass = equilinox_options.EquilinoxOptions
    options: equilinox_options.EquilinoxOptions  # Common mistake: This has to be a colon (:), not an equals sign (=).

    SpeciesUtils.all_species = SpeciesUtils.get_species()

    items.set_item_names_to_id()
    Tasks.init_tasks()

    location_name_to_id = locations.get_loc_names_to_id_dict()
    item_name_to_id = items.ITEM_NAME_TO_ID

    origin_region_name = "Menu"

    def generate_early(self) -> None:
        self.push_precollected(self.create_item("Grass Tuft Permit"))
        starting_dp_values = items.approx_money_as_sum(self.options.starting_dp.value - 2500, 6)
        for amt in starting_dp_values:
            self.push_precollected(items.get_nearest_money_item(self, amt))
        return

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.EquilinoxItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict("tasks_reward_dp", "starting_dp", "itempool_dp")

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> Any:
        return slot_data

    def explain_rule(self, location_name: str, state: CollectionState) -> list[JSONMessagePart]:
        if not location_name:
            return [
                {
                    "type": "text",
                    "text": "Enter a location to get an explanation",
                }
            ]
        all_location_names = set(self.multiworld.regions.location_cache[self.player])
        guess, usable, response = get_intended_text(location_name, all_location_names)
        if not usable:
            return [{"type": "text", "text": response}]

        location_name = guess
        location = self.get_location(location_name)
        accessible = location.can_reach(state)
        messages: list[JSONMessagePart] = [
            {"type": "text", "text": "Location "},
            {"type": "color", "color": "green" if accessible else "salmon", "text": f"{location_name}"},
            {"type": "text", "text": ": "},
        ]

        if "Complete Task" in location_name:
            task_name = location_name.replace("Complete Task '", "")[:-1]
            task = Tasks.get_task_from_name(task_name)
            if task is None:
                messages.append({"type": "text", "text": "No task with this name found?"})
                return messages

            if task.required_species:
                categories = task.required_species.split(";")
                species_lists = task.get_required_species()
                if task.requires_species_satisfaction:
                    title = "\nRequires Species (with satisfaction):"
                else:
                    title = "\nRequires Species:"
                messages.append({"type": "text", "text": title})

                for cat_index in range(len(categories)):
                    if len(species_lists[cat_index]) == 0: continue
                    if len(species_lists[cat_index]) == 1:
                        species = species_lists[cat_index][0]
                        if species.is_base_species():
                            has_prereq = state.has(f"{species.name} Permit", self.player)
                            messages.append({"type": "color", "color": "green" if has_prereq else "salmon",
                                             "text": f"\n    {species.name}"})
                            if not has_prereq: messages.append({"type": "text", "text": f" (missing unlock permit)"})
                        else:
                            has_prereq = self.get_location(f"Evolve {species.name}").can_reach(state)
                            messages.append({"type": "color", "color": "green" if has_prereq else "salmon",
                                             "text": f"\n    {species.name}"})
                            if not has_prereq: messages.append({"type": "text", "text": f" (evolution not in logic)"})
                    else:
                        has_prereq = False
                        for species in species_lists[cat_index]:
                            if species.is_base_species():
                                has_prereq |= state.has(f"{species.name} Permit", self.player)
                            else:
                                has_prereq |= self.get_location(f"Evolve {species.name}").can_reach(state)
                        messages.append({"type": "color", "color": "green" if has_prereq else "salmon",
                                         "text": f"\n    {categories[cat_index]}"})
        elif "Evolve" in location_name:
            species_name = location_name.replace("Evolve ", "")
            species = SpeciesUtils.get_species_from_name(species_name)
            if species is None:
                messages.append({"type": "text", "text": "No species with this name found?"})
                return messages
            previous_evo = species.get_previous_evolution()
            messages.append({"type": "text", "text": f"\nEvolves From: "})
            if previous_evo.is_base_species():
                has_prereq = state.has(f"{previous_evo.name} Permit", self.player)
                messages.append({"type": "color", "color": "green" if has_prereq else "salmon", "text": previous_evo.name})
                if not has_prereq: messages.append({"type": "text", "text": f" (missing unlock permit)"})
            else:
                has_prereq = self.get_location(f"Evolve {previous_evo.name}").can_reach(state)
                messages.append({"type": "color", "color": "green" if has_prereq else "salmon", "text": previous_evo.name})
                if not has_prereq: messages.append({"type": "text", "text": f" (evolution not in logic)"})
            messages.append({"type": "text", "text": f"\nEvolution Requirements: "})
            if len(species.evolution_requirements) == 0:
                messages.append({"type": "color", "color": "green", "text": "None"})
            else:
                for evo_req in species.evolution_requirements:
                    messages.extend(evo_req.explain(self, species, state))
        else:
            messages.append({"type": "text", "text": "Unknown location type"})

        return messages