from __future__ import annotations

import json
import pkgutil

from . import Evolution
from . import SpeciesUtils

all_tasks: list[Task] = []

class Task:
    def __init__(self,
                 name: str,
                 repeatable: bool,
                 required_species: str,
                 requires_species_satisfaction: bool,
                 id: int):
        self.name = name
        self.repeatable = repeatable
        self.required_species = required_species
        self.requires_species_satisfaction = requires_species_satisfaction
        self.id = id

    def get_required_species(self) -> list[list[SpeciesUtils.Species | None]]:
        return SpeciesUtils.get_required_species_from_string(self.required_species)

def task_object_decoder(t_obj) -> Task:
    return Task(t_obj["name"], t_obj["repeatable"], t_obj["required_species"], t_obj["requires_species_satisfaction"], t_obj["id"])

def init_tasks() -> None:
    global all_tasks
    tasks_raw_data = pkgutil.get_data(__name__, "data/tasks.json")
    if not tasks_raw_data:
        return

    raw_list = json.loads(tasks_raw_data)

    task_list = [task_object_decoder(item) for item in raw_list]
    all_tasks = task_list