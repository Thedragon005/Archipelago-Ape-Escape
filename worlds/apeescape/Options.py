from __future__ import annotations

from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions


class GoalOption(Choice):
    """Choose end goal

        first: First final boss at Monkey Madness
        second: 100% boss at Peak Point Matrix

        Supported values: first, second
        Default value: first
    """

    display_name = "Goal"
    option_first = 0x00
    option_second = 0x01
    default = option_first


class LogicOption(Choice):
    """Choose expected trick knowledge

        glitchless: no glitches required
        noij: all glitches except infinite jump
        ij: all glitches

        Supported values: glitchless, noij, ij
        Default value: glitchless
    """

    display_name = "Logic"
    option_glitchless = 0x00
    option_noij = 0x01
    option_ij = 0x02
    default = option_glitchless


class EntranceOption(Choice):
    """Choose if level entrances should be randomized.

        off: levels will be in the vanilla order
        levels: the 19 main levels will be shuffled between each other
        levelsraces: the 19 main levels and 2 Jake races will be shuffled

        Supported values: off, levels, races
        Default value: levels
    """

    display_name = "Entrance"
    option_off = 0x00
    option_levels = 0x01
    option_levelsraces = 0x02
    default = option_levels


class KeyOption(Choice):
    """Choose how many levels each World Key should unlock. The first three levels will always start unlocked.
        Peak Point Matrix will always require the same number of World Keys as the Monkey Madness entrance.

        world: each World Key unlocks the 3 levels in a world. Races are unlocked with the world after them. Creates 6 World Keys.
        worldandraces: each World Key unlocks the 3 levels in a world. Races are counted as worlds. Creates 8 World Keys.
        level: each World Key unlocks the next level. Races are unlocked with the level after them. Creates 16 World Keys.
        levelandraces: each World Key unlocks the next level. Races are counted as levels. Creates 18 World Keys.

        Supported values: world, worldandraces, level, levelandraces
        Default value: world
    """

    display_name = "Unlocks per Key"
    option_world = 0x00
    option_worldandraces = 0x01
    option_level = 0x02
    option_levelandraces = 0x03
    default = option_world


class CoinOption(Choice):
    """Choose if Specter Coins should act as Locations

        true: coins are added as locations
        false: coins are not added as locations

        Supported values: true, false
        Default value: false
    """

    display_name = "Coin"
    option_true = 0x01
    option_false = 0x00
    default = option_false


class MailboxOption(Choice):
    """Choose if mailboxes should act as locations.
        Mailboxes in training rooms will never be locations.

        true: mailboxes are added as locations
        false: mailboxes are not added as locations

        Supported values: true, false
        Default value: false
    """

    display_name = "Mailbox"
    option_true = 0x01
    option_false = 0x00
    default = option_false


class GadgetOption(Choice):
    """Choose the starting gadget. The Time Net will always be a starting gadget.
    
        club: start with the Stun Club
        radar: start with the Monkey Radar
        sling: start with the Slingback Shooter
        hoop: start with the Super Hoop
        flyer: start with the Sky Flyer
        car: start with the RC Car
        punch: start with the Magic Punch
        none: start with no additional gadgets

        Supported values: club, radar, sling, hoop, flyer, car, punch, none
        Default value: club
    """
    
    display_name = "Gadget"
    option_club = 0x00
    option_radar = 0x01
    option_sling = 0x02
    option_hoop = 0x03
    option_flyer = 0x04
    option_car = 0x05
    option_punch = 0x06
    option_none = 0x08
    default = option_club


class SuperFlyerOption(Choice):
    """Choose if the Super Flyer trick should be put into logic

        true: super flyer is put into logic
        false: super flyer is not put into logic

        Supported values: true, false
        Default value: false
    """
    display_name = "Super Flyer"
    option_true = 0x01
    option_false = 0x00
    default = option_false

class ShuffleWaterNetOption(Choice):
    """Choose if the Water Net should be shuffled.
        This option splits the Water Net item to 2 distinct items:
        Progressive Water Net : having 1 gives the ability to Swim, having 2 gives the ability to Dive
        Water Catch : Can shoot your Net in water to catch the Monkeys

        true: Water Net is shuffled, adding Progressive Water Net and Water Catch the the pool
        false: Water Net is not shuffled, and is given at game start.

        Supported values: true, false
        Default value: false
    """
    display_name = "Shuffle Water Net"
    option_true = 0x01
    option_false = 0x00
    default = option_false

class ShuffleNetOption(Choice):
    """Choose if the Time Net should be shuffled.
        This option requires at least one of coins and mailboxes to be shuffled to be used - if all locations in this world require the net, the net will be given at game start.

        true: Time Net is shuffled into the pool. The mailboxes in the Time Station will also be locations if this happens.
        false: Time Net is not shuffled, and is given at game start.

        Supported values: true, false
        Default value: false
    """
    display_name = "Shuffle Net"
    option_true = 0x01
    option_false = 0x00
    default = option_false


@dataclass
class ApeEscapeOptions(PerGameCommonOptions):
    goal: GoalOption
    logic: LogicOption
    entrance: EntranceOption
    unlocksperkey: KeyOption
    coin: CoinOption
    mailbox: MailboxOption
    gadget: GadgetOption
    superflyer: SuperFlyerOption
    shufflenet: ShuffleNetOption
    shufflewaternet: ShuffleWaterNetOption
