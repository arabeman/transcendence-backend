from classes import Hero
from typing import List

HEROES: List[Hero] = [
	Hero(
        id = 1,
        nickname = "Gale",
        fullname = "Gale Hawthorne",
        occupation = ["Wizard", "Adventurer", "Master"],
        powers = ["Magic", "Intelligence", "Charisma"],
        hobby = ["Studying magic", "Cooking"],
        type = "Wizard",
        rank = 54
    ),
	Hero(
        id = 2,
        nickname = "Nyx",
        fullname = "Nyx Blackwater",
        occupation = ["Assassin", "Scout"],
        powers = ["Stealth", "Shadowstep", "Daggers"],
        hobby = ["Night running", "Lockpicking"],
        type = "Rogue",
        rank = 48
    ),
    Hero(
        id = 3,
        nickname = "Brann",
        fullname = "Brann Ironfist",
        occupation = ["Mercenary", "Smith"],
        powers = ["Strength", "Warhammer", "Endurance"],
        hobby = ["Forging steel", "Arm-wrestling"],
        type = "Warrior",
        rank = 51
    ),
    Hero(
        id = 4,
        nickname = "Lyra",
        fullname = "Lyra Windrunner",
        occupation = ["Ranger", "Guide"],
        powers = ["Archery", "Hawkeye", "Beast bond"],
        hobby = ["Falconry", "Map making"],
        type = "Archer",
        rank = 46
    ),
    Hero(
        id = 5,
        nickname = "Vale",
        fullname = "Vale Stormborn",
        occupation = ["Elementalist", "Scholar"],
        powers = ["Lightning", "Wind", "Barrier"],
        hobby = ["Storm watching", "Ancient lore"],
        type = "Mage",
        rank = 57
    ),
    Hero(
        id = 6,
        nickname = "Mira",
        fullname = "Mira Sunblade",
        occupation = ["Paladin", "Healer"],
        powers = ["Radiance", "Shielding", "Healing"],
        hobby = ["Herbalism", "Chanting"],
        type = "Paladin",
        rank = 60
    ),
    Hero(
        id = 7,
        nickname = "Tova",
        fullname = "Tova Ember",
        occupation = ["Alchemist", "Inventor"],
        powers = ["Firebombs", "Acid vials", "Tinkering"],
        hobby = ["Foraging reagents", "Sketching schematics"],
        type = "Alchemist",
        rank = 43
    ),
    Hero(
        id = 8,
        nickname = "Orion",
        fullname = "Orion Flux",
        occupation = ["Technomancer", "Strategist"],
        powers = ["Electroshock", "Drones", "Holo-maps"],
        hobby = ["Star charts", "Circuit carving"],
        type = "Tech-Mage",
        rank = 58
    ),
    Hero(
        id = 9,
        nickname = "Seren",
        fullname = "Seren Tidecaller",
        occupation = ["Druid", "Mediator"],
        powers = ["Water shaping", "Vine whip", "Soothing song"],
        hobby = ["River walks", "Shell collecting"],
        type = "Druid",
        rank = 44
    ),
    Hero(
        id = 10,
        nickname = "Knox",
        fullname = "Knox Gearhart",
        occupation = ["Engineer", "Guardian"],
        powers = ["Exo-armor", "Rail punch", "Fortification"],
        hobby = ["Blueprint drafting", "Metal puzzles"],
        type = "Guardian",
        rank = 52
    )
]
