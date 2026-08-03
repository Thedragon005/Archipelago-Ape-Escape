"""
Plain-Python trap helpers -- deliberately has NO kivy/kivymd imports.
Safe to import at the top of Client.py; trap_tab.py (the kivy widget) is
NOT safe to import at the top, since kvui.py must be the first thing to
touch kivy. See trap_tab.py's docstring / TrapSenderClient.py's make_gui().
"""

# Traps excluded from both the auto-sender and the manual Traps tab.
# Palm Punch Trap: [add the actual reason here, e.g. "softlocks in the
# current Ape Escape implementation" -- whatever it was originally for]
EXCLUDED_TRAPS = ["Palm Punch Trap"]


def get_trap_names(world, exclude=EXCLUDED_TRAPS):
    """
    Same logic your autoplayer() already uses: substring match against
    world.item_names (the static, per-game name list -- works even when
    the seed has traps disabled, since it isn't limited to placed items).
    """
    return sorted(x for x in world.item_names if "Trap" in x and x not in exclude)
