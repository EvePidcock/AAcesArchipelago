from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from pkgutil import get_data

from . import items

import json, os

if TYPE_CHECKING:
    from .world import EarthWorld

# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.

# ID Format: XXYYZZZ
#
# XX:
#   10 = System Upgrades
#        YY: Tier
#           10 = Green 1, 20 = Green 2, 30 = Green 3, 40 = Red 1, 50 = Red 2, 60 = Red 3
#        ZZZ: id
#
#   11 = Earning Green/Red Trains
#       YY: Green (10) or Red (20)
#       ZZZ: Count
LOCATION_NAME_TO_ID = {

    # Point Checks (10XXX)
    "Score 50 Points": 10050,
    "Score 100 Points": 10100,
    "Score 150 Points": 10150,
    "Score 200 Points": 10200,

    # Fauna Checks (20XXX)
    "Hedgehog Claim": 20001,
    "Dung Beetle Claim": 20002,
    "American Bison Claim": 20003,
    "Red Deer Claim": 20004,
    "Lubber Grasshopper Claim": 20005,
    "Wild Boar Claim": 20006,
    "Andean Condor Claim": 20007,
    "Green Tree Ant Claim": 20008,
    "Bald Eagle Claim": 20009,
    "Pale-Billed Woodpecker Claim": 20010,
    "Green Iguana Claim": 20011,
    "Spotted Hyena Claim": 20012,
    "Red Squirrel Claim": 20013,
    "Yellow-Bellied Marmot Claim": 20014,
    "Brown-Throated Sloth Claim": 20015,
    "Western Moose Claim": 20016,
    "Sri Lankan Leopard Claim": 20017,
    "Atlantic Puffin Claim": 20018,
    "Earthworm Claim": 20019,
    "European Mole Claim": 20020,
    "Barn Owl Claim": 20021,
    "Talamanca Hummingbird Claim": 20022,
    "Echidna Claim": 20023,
    "Kingfisher Claim": 20024,
    "Rainbow Shield Bug Claim": 20025,
    "Arctic Tern Claim": 20026,
    "Margay Claim": 20027,
    "Praying Mantis Claim": 20028,
    "Yellow Cheeked Gibbon Claim": 20029,
    "Hippopotamus Claim": 20030,
    "Indonesian Pit Viper Claim": 20031,
    "King Penguin Claim": 20032,
    "Siamese Rhinoceros Claim": 20033,
    "Wood Duck Claim": 20034,
    "Grey Wolf Claim": 20035,
    "Seven-Spotted Ladybug Claim": 20036,
    "Mountain Gorilla Claim": 20037,
    "Black Wildebeest Claim": 20038,
    "Bornean Orangutan Claim": 20039,
    "Siberian Tiger Claim": 20040,
    "Mountain Lion Claim": 20041,
    "Plains Zebra Claim": 20042,
    "Northern Giraffe Claim": 20043,
    "Cairns Birdwing Butterfly Claim": 20044,
    "Red-Eyed Tree Frog Claim": 20045,
    "Brown Bear Claim": 20046,
    "Fire Salamander Claim": 20047,
    "Panther Chameleon Claim": 20048,
    "Western Honeybee Claim": 20049,
    "African Bush Elephant Claim": 20050,
    "Arctic Fox Claim": 20051,
    "American Alligator Claim": 20052,

    # Ecosystem Checks (30XXX) -- Cols/rows = 18, diagonals = 24, flora count = 28, habitat = 18, font = 18
    "Finland Snow Forest (18 pts)": 30001,
    "Chic-Choc Mountains (18 pts)": 30002,
    "Irati (18 pts)": 30003,
    "Odisha Semi-Evergreen (21 pts)": 30004,
    "Daintree (24 pts)": 30005,
    "Blackforest (28 pts)": 30006,
    "Reunion Island (20 pts)": 30007,
    "Sakurajima (18 pts)": 30008,
    "Namib Desert (18 pts)": 30009,
    "Denali National Park (18 pts)": 30010,
    "Monteverde Cloud Forest (28 pts)": 30011,
    "Everglades (24 pts)": 30012,
    "Amazon Rain Forest (24 pts)": 30013,
    "Borneo Lowland Rain Forest (24 pts)": 30014,
    "MacMillan Park (20 pts)": 30015,
    "Great Basin Desert (18 pts)": 30016,
    "Ngorongoro Crater (18 pts)": 30017,
    "Waiotapu (18 pts)": 30018,
    "Tasmanian Temperate Rain Forest (18 pts)": 30019,
    "Batanta Island (18 pts)": 30020,
    "Mauna Kea (18 pts)": 30021,
    "Aconcagua (18 pts)": 30022,
    "Bashkiriya National Park (20 pts)": 30023,
    "Valin Mountain (20 pts)": 30024,
    "Arabian Desert (20 pts)": 30025,
    "Bhutan Rain Forest (24 pts)": 30026,
    "Tai Poutini National Park (18 pts)": 30027,
    "Madagascar Humid Canopy (18 pts)": 30028,
    "Great Hungarian Plain (28 pts)": 30029,
    "Caerlaverock Nature Reserve (24 pts)": 30030,
    "Yuanjiang Savanna (18 pts)": 30031,
    "Sierra Nevada de Santa Marta (18 pts)": 30032,
    "Knysna-Amatole Forests (18 pts)": 30033,
    "Jiuzhaigou Valley (22 pts)": 30034,
    "Tongass National Forest (18 pts)": 30035,
    "Bwindi Impenetrable Forest (18 pts)": 30036,
    "New Guinea Rain Forest (20 pts)": 30037,
    "Atacama Desert (24 pts)": 30038,
    "Twin Islands (20 pts)": 30039,
    "Lonely Island (20 pts)": 30040,
    "Serengeti (18 pts)": 30041,
    "Okavango (18 pts)": 30042,
    "Antarctica (18 pts)": 30043,
    "Great Plains (24 pts)": 30044,
    "Himalayas (21 pts)": 30045,
    "Alps (21 pts)": 30046,
    "Thai Highlands (18 pts)": 30047,
    "Sudd Swamp (18 pts)": 30048,
    "Tangkoko Nature Reserve (24 pts)": 30049,
    "Siberian Taiga (20 pts)": 30050,
    "Australian Temperate Forest (21 pts)": 30051,
    "Yagishiri Island (20 pts)": 30052,
    "Mount Kilimanjaro (20 pts)": 30053,
    "Indian Evergreen Forest (30 pts)": 30054,
    "Mbeliling Mountain (18 pts)": 30055,
    "Atlas Mountains (18 pts)": 30056,
    "Rocky Mountains (18 pts)": 30057,
    "Nile Delta (18 pts)": 30058,
    "Redwood National Park (18 pts)": 30059,
    "Congolian Rain Forest (20 pts)": 30060,
    "Yellowstone Caldera (18 pts)": 30061,
    "Angat Watershed Forest (25 pts)": 30062,
    "Great Steppe (28 pts)": 30063,
    "Florida Scrub (24 pts)": 30064,
    "Okefenokee Swamp (14 pts)": 30065,
    "Magdelen Islands (20 pts)": 30066,
    "Miyawaki Forest (20 pts)": 30067,
    "Quiver Tree Forest (20 pts)": 30068,
    "St-Hilaire Mount (20 pts)": 30069,
    "Khao Yai (20 pts)": 30070
}


# Each Location instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Location class and override the "game" field.
class EarthLocation(Location):
    game = "Earth"


# Let's make one more helper method before we begin actually creating locations.
# Later on in the code, we'll want specific subsections of LOCATION_NAME_TO_ID.
# To reduce the chance of copy-paste errors writing something like {"Chest": LOCATION_NAME_TO_ID["Chest"]},
# let's make a helper method that takes a list of location names and returns them as a dict with their IDs.
# Note: There is a minor typing quirk here. Some functions want location addresses to be an "int | None",
# so while our function here only ever returns dict[str, int], we annotate it as dict[str, int | None].
def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: EarthWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: EarthWorld) -> None:
    # Finally, we need to put the Locations ("checks") into their regions.
    # Once again, before we do anything, we can grab our regions we created by using world.get_region()
    # Create card locations
    CARD_NAME_TO_ID = {}
    EVENT_NAME_TO_ID = {}

    earth_cards = get_data(__name__, "earthCards.txt").decode("utf-8").strip().split("\n")
    card_id = 40000

    for line in earth_cards:
        card = json.loads(line.strip())
        card_id += 1
        CARD_NAME_TO_ID.update({f"Play card \"{card['Name']}\"": card_id})

    event_cards = get_data(__name__, "eventCards.txt").decode("utf-8").strip().split("\n")
    card_id = 41000

    for line in event_cards:
        card = json.loads(line.strip())
        card_id += 1
        EVENT_NAME_TO_ID.update({f"Play event \"{card['Name']}\"": card_id})

    world.get_region("Main").add_locations(CARD_NAME_TO_ID)
    world.get_region("Main").add_locations(LOCATION_NAME_TO_ID)
    world.get_region("Events").add_locations(EVENT_NAME_TO_ID)

    LOCATION_NAME_TO_ID.update(CARD_NAME_TO_ID)
    LOCATION_NAME_TO_ID.update(EVENT_NAME_TO_ID)




def create_events(world: EarthWorld) -> None:
    # Sometimes, the player may perform in-game actions that allow them to progress which are not related to Items.
    # In our case, the player must press a button in the top left room to open the final boss door.
    # AP has something for this purpose: "Event locations" and "Event items".
    # An event location is no different than a regular location, except it has the address "None".
    # It is treated during generation like any other location, but then it is discarded.
    # This location cannot be "sent" and its item cannot be "received", but the item can be used in logic rules.
    # Since we are creating more locations and adding them to regions, we need to grab those regions again first.
    #top_left_room = world.get_region("Top Left Room")
    #final_boss_room = world.get_region("Final Boss Room")

    # One way to create an event is simply to use one of the normal methods of creating a location.
    #button_in_top_left_room = RailRouteLocation(world.player, "Top Left Room Button", None, top_left_room)
    #top_left_room.locations.append(button_in_top_left_room)

    # We then need to put an event item onto the location.
    # An event item is an item whose code is "None" (same as the event location's address),
    # and whose classification is "progression". Item creation will be discussed more in items.py.
    # Note: Usually, items are created in world.create_items(), which for us happens in items.py.
    # However, when the location of an item is known ahead of time (as is the case with an event location/item pair),
    # it is common practice to create the item when creating the location.
    # Since locations also have to be finalized after world.create_regions(), which runs before world.create_items(),
    # we'll create both the event location and the event item in our locations.py code.
    #button_item = items.RailRouteItem("Top Left Room Button Pressed", ItemClassification.progression, None, world.player)
    #button_in_top_left_room.place_locked_item(button_item)

    # A way simpler way to do create an event location/item pair is by using the region.create_event helper.
    # Luckily, we have another event we want to create: The Victory event.
    # We will use this event to track whether the player can win the game.
    # The Victory event is a completely optional abstraction - This will be discussed more in set_rules().
    world.get_region("Events").add_event(
        "Game finished", "Victory", location_type=EarthLocation, item_type=items.EarthItem
    )

    # If you create all your regions and locations line-by-line like this,
    # the length of your create_regions might get out of hand.
    # Many worlds use more data-driven approaches using dataclasses or NamedTuples.
    # However, it is worth understanding how the actual creation of regions and locations works,
    # That way, we're not just mindlessly copy-pasting! :)
    return