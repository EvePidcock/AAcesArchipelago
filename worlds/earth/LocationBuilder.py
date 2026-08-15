import json
import pkgutil
from enum import Enum
from typing import List


class EarthLocType(Enum):
    CARD = 1
    EVENT = 2
    ECOSYSTEM = 3
    FAUNA = 4

class EcoOrFaunaLoc:
    def __init__(self, name: str, loc_type: EarthLocType, points: int, needs_events: bool, red_calls: int, blue_calls: int, yellow_calls: int, needed_cards: int, id: int):
        self.name = name
        self.loc_type = loc_type
        self.points = points
        self.needs_events = needs_events
        self.red_calls = red_calls
        self.blue_calls = blue_calls
        self.yellow_calls = yellow_calls
        self.needed_cards = needed_cards
        self.id = id
    # name: str
    # points: int
    # needs_events: bool
    # red_calls, blue_calls, yellow_calls: int
    # needed_cards: int
    # id: int (long)

class EcosystemLoc(EcoOrFaunaLoc):
    def __init__(self, name, points, needs_events, red_calls, blue_calls, yellow_calls, needed_cards, id):
        super().__init__(name, EarthLocType.ECOSYSTEM, points, needs_events, red_calls, blue_calls, yellow_calls, needed_cards, id)
    # name: str
    # points: int
    # needs_events: bool
    # red_calls, blue_calls, yellow_calls: int
    # needed_cards: int
    # id: int (long)

def ecosystem_obj_decoder(l_obj):
    return EcosystemLoc(l_obj['name'], l_obj['points'], l_obj['needs_event_cards'], l_obj['red_calls'], l_obj['blue_calls'], l_obj['yellow_calls'], l_obj['played_cards_needed'], l_obj['id'])

def get_ecosystem_locs() -> list[EcosystemLoc]:
    ecosystem_raw_data = pkgutil.get_data(
        __name__, "data/ecosystems.json")
    if ecosystem_raw_data:
        location_data = json.loads(
            ecosystem_raw_data, object_hook=ecosystem_obj_decoder)
        eco_list: List[EcosystemLoc] = list(location_data)
        return eco_list
    empty_list: List[EcosystemLoc] = []
    return empty_list

def get_loc_name_from_obj(loc: EcoOrFaunaLoc) -> str:
    if loc.loc_type == EarthLocType.ECOSYSTEM:
        return f"{loc.name} ({loc.points} pts)"
    elif loc.loc_type == EarthLocType.FAUNA:
        return f"{loc.name} Claim"
    elif loc.loc_type == EarthLocType.CARD:
        return f"Play card {loc.name}"
    elif loc.loc_type == EarthLocType.EVENT:
        return f"Play event {loc.name}"
    else:
        return ""

class FaunaLoc(EcoOrFaunaLoc):
    def __init__(self, name, needs_events, red_calls, blue_calls, yellow_calls, needed_cards, id):
        super().__init__(name, EarthLocType.FAUNA, 0, needs_events, red_calls, blue_calls, yellow_calls, needed_cards, id)
    # name: str
    # needs_events: bool
    # red_calls, blue_calls, yellow_calls: int
    # needed_cards: int
    # id: int (long)

def fauna_obj_decoder(l_obj):
    return FaunaLoc(l_obj['name'], l_obj['needs_event_cards'], l_obj['red_calls'], l_obj['blue_calls'], l_obj['yellow_calls'], l_obj['played_cards_needed'], l_obj['id'])

def get_fauna_locs() -> list[FaunaLoc]:
    fauna_raw_data = pkgutil.get_data(
        __name__, "data/fauna.json")
    if fauna_raw_data:
        location_data = json.loads(
            fauna_raw_data, object_hook=fauna_obj_decoder)
        fauna_list: List[FaunaLoc] = list(location_data)
        return fauna_list
    empty_list: List[FaunaLoc] = []
    return empty_list

#Not actually used yet
class CardLoc:
    def __init__(self, name: str, event: bool, id: int):
        self.name = name
        self.event = event
        self.id = id