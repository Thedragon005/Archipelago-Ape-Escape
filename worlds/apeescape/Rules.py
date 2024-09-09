from typing import TYPE_CHECKING

from .RulesGlitchless import set_glitchless_rules
from .RulesNoIJ import set_noij_rules
from .RulesIJ import set_ij_rules

if TYPE_CHECKING:
    from . import ApeEscapeWorld


def set_rules(world: "ApeEscapeWorld"):
    if world.options.logic == "glitchless":
        set_glitchless_rules(world)
    elif world.options.logic == "noij":
        set_noij_rules(world)
    elif world.options.logic == "ij":
        set_ij_rules(world)
