from __future__ import annotations

from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions


class DebugOption(Choice):
    """Choose current Debug Settings

        Off: No debug settings
        Early Items: Gadgets will be placed in first two levels
        Early Keys: Keys will be placed in the first two levels

        Supported values: off, item, key
        Default value: off
        """

    display_name = "Debug Option"
    option_off = 0x00
    option_item = 0x01
    option_key = 0x02
    default = option_off


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
    display_name = "SuperFlyer"
    option_true = 0x01
    option_false = 0x00
    default = option_false


@dataclass
class ApeEscapeOptions(PerGameCommonOptions):
    debug: DebugOption
    goal: GoalOption
    logic: LogicOption
    coin: CoinOption
    gadget: GadgetOption
    superflyer: SuperFlyerOption
