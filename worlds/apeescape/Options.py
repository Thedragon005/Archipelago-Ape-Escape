from __future__ import annotations

from dataclasses import dataclass
from Options import Choice, DeathLink, PerGameCommonOptions


class GoalOption(Choice):
    """Choose the victory condition for this world.

        first: First Specter fight in Monkey Madness.
        second: Second Specter fight in Peak Point Matrix.

        Supported values: first, second
        Default value: first
    """

    display_name = "Goal"
    option_first = 0x00
    option_second = 0x01
    default = option_first


class LogicOption(Choice):
    """Choose expected trick knowledge.

        glitchless: No glitches required.
        noij: Almost all tricks and glitches can be required, except infinite jump.
        ij: All tricks and glitches can be required.

        Supported values: glitchless, noij, ij
        Default value: glitchless
    """

    display_name = "Logic"
    option_glitchless = 0x00
    option_noij = 0x01
    option_ij = 0x02
    default = option_glitchless


class SuperFlyerOption(Choice):
    """Choose if the Super Flyer trick should be put into logic.

        false: Super Flyer is not put into logic.
        true: Super Flyer is put into logic.

        Supported values: false, true
        Default value: false
    """
    display_name = "Super Flyer"
    option_false = 0x00
    option_true = 0x01
    default = option_false


class EntranceOption(Choice):
    """Choose which level entrances should be randomized. Peak Point Matrix will always be the last level.

        none: Levels will be in the vanilla order.
        eras: The 18 main levels (all except Monkey Madness) will be shuffled.
        erasraces: The 18 main levels (all except Monkey Madness) and 2 Jake races will be shuffled.
        levels: The 19 main levels will be shuffled.
        levelsraces: The 19 main levels and 2 Jake races will be shuffled.

        Supported values: none, eras, erasraces, levels, levelsraces
        Default value: levels
    """

    display_name = "Entrance"
    option_none = 0x00
    option_eras = 0x01
    option_erasraces = 0x02
    option_levels = 0x03
    option_levelsraces = 0x04
    default = option_none


class KeyOption(Choice):
    """Choose how many levels each World Key should unlock. The first three levels will always start unlocked.
        Peak Point Matrix will always require the same number of World Keys as the Monkey Madness entrance.

        world: Each World Key unlocks the 3 levels in a world. Races are unlocked with the world after them. Creates 6 World Keys.
        worldandraces: Each World Key unlocks the 3 levels in a world. Races are counted as worlds. Creates 8 World Keys.
        level: Each World Key unlocks the next level. Races are unlocked with the level after them. Creates 16 World Keys.
        levelandraces: Each World Key unlocks the next level. Races are counted as levels. Creates 18 World Keys.

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
    """Choose if Specter Coins should be added as locations.

        false: Specter Coins are not locations.
        true: The 60 Specter Coins are added as locations.

        Supported values: false, true
        Default value: false
    """

    display_name = "Coin"
    option_false = 0x00
    option_true = 0x01
    default = option_false


class MailboxOption(Choice):
    """Choose if mailboxes should act as locations.
        Mailboxes in training rooms will never be locations.

        false: Mailboxes are not locations.
        true: The 63 available mailboxes are added as locations.

        Supported values: false, true
        Default value: false
    """

    display_name = "Mailbox"
    option_false = 0x00
    option_true = 0x01
    default = option_false


class GadgetOption(Choice):
    """Choose the starting gadget from the non-net gadgets.
    
        club: Start with the Stun Club.
        radar: Start with the Monkey Radar.
        sling: Start with the Slingback Shooter.
        hoop: Start with the Super Hoop.
        flyer: Start with the Sky Flyer.
        car: Start with the RC Car.
        punch: Start with the Magic Punch.
        none: Start with no additional gadgets.

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


class ShuffleNetOption(Choice):
    """Choose if the Time Net should be shuffled.
        This option requires at least one of coins and mailboxes to be shuffled to be used - if all locations in this world require the net, the net will be given at game start.

        false: Time Net is not shuffled, and is given at game start.
        true: Time Net is shuffled into the pool. The mailboxes in the Time Station will also be locations if this happens.

        Supported values: false, true
        Default value: false
    """
    display_name = "Shuffle Net"
    option_false = 0x00
    option_true = 0x01
    default = option_false


class ShuffleWaterNetOption(Choice):
    """Choose if the Water Net should be shuffled.

        off: Water Net is not shuffled, and is given at game start.
        progressive: Water Net is shuffled and split into parts, adding two Progressive Water Net and Water Catch to the pool.
        - Progressive Water Net : The first allows Spike to swim on the surface and avoid drowning after a few seconds. The second allows Spike to dive underwater.
        - Water Catch: Allows shooting the Water Net.
        on: Water Net is shuffled, adding it to the pool.


        Supported values: off, progressive, on
        Default value: off
    """
    display_name = "Shuffle Water Net"
    option_off = 0x00
    option_progressive = 0x01
    option_on = 0x02
    default = option_off

class LowOxygenSounds(Choice):
    """How quickly the oxygen beep sound effect will play

        off: Low Oxygen sounds will not play at all.
        half: Frequency of Low Oxygen sounds will be cut in half
        on: Low Oxygen Sounds will play as vanilla


        Supported values: off, half, on
        Default value: off
    """
    display_name = "Low Oxygen Sounds"
    option_off = 0x00
    option_half = 0x01
    option_on = 0x02
    default = option_on


@dataclass
class ApeEscapeOptions(PerGameCommonOptions):
    goal: GoalOption
    logic: LogicOption
    superflyer: SuperFlyerOption
    entrance: EntranceOption
    unlocksperkey: KeyOption
    coin: CoinOption
    mailbox: MailboxOption
    gadget: GadgetOption
    shufflenet: ShuffleNetOption
    shufflewaternet: ShuffleWaterNetOption
    lowoxygensounds: LowOxygenSounds
    death_link: DeathLink
