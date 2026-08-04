"""
Traps tab widget (kivymd-based) for TrapSenderContext.

IMPORTANT: this module imports kivy/kivymd/kvui at module level, so it must
only ever be imported lazily, from inside make_gui() -- AFTER
super().make_gui() has already caused kvui to load kivy first. See
TrapSenderClient.py's make_gui() for the exact pattern. Never import this
module at the top of Client.py.
"""

import logging
import asyncio
from kivy.metrics import dp
from kivy.clock import mainthread
from kivy.core.text import Label as CoreLabel
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.textinput import TextInput
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.app import MDApp
from kvui import UILog

# Import safe non-kivy helpers using relative import
from .trap_utils import DISABLED_TRAPS, set_trap_disabled

# Default font size trap button labels render at (kept in one place so the
# width measurement below always matches what's actually on screen).
TRAP_BUTTON_FONT_SIZE = dp(14)


def _measure_text_width(text, font_size=TRAP_BUTTON_FONT_SIZE):
    """Measures text width."""
    label = CoreLabel(text=text, font_size=font_size)
    label.refresh()
    return label.texture.size[0]


class TrapButton(ButtonBehavior, MDBoxLayout):
    """Custom trap button."""

    def __init__(self, text="", **kwargs):
        super().__init__(**kwargs)
        self.radius = [self.height / 2] if self.height else [dp(18)]
        self.bind(height=lambda *_: setattr(self, "radius", [self.height / 2]))
        self.is_blocked = False

        self._label = MDLabel(
            text=text,
            halign="center",
            valign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_size=TRAP_BUTTON_FONT_SIZE,
        )
        self._label.bind(size=lambda s, v: setattr(s, "text_size", v))
        self.add_widget(self._label)

    def update_state(self, is_blocked):
        """Updates button color and state."""
        self.is_blocked = is_blocked
        self.disabled = is_blocked

        if self.is_blocked:
            self.md_bg_color = (0.2, 0.2, 0.2, 1)  # Muted dark grey
            self._label.text_color = (0.6, 0.6, 0.6, 1)  # Dim grey text
        else:
            self.md_bg_color = (0.15, 0.25, 0.35, 1)  # Steel blue/grey base (highly readable)
            self._label.text_color = (1, 1, 1, 1)  # Solid white text


class TrapPanel(MDBoxLayout):
    """Main panel for traps and logs."""

    def __init__(self, trap_list=None, log_logger_name="TrapSender", **kwargs):
        super().__init__(orientation="horizontal", **kwargs)
        self.trap_list = trap_list or []

        # --- left column: 50% width ---
        left = MDBoxLayout(orientation="vertical", size_hint_x=0.5, spacing=dp(4), padding=dp(4))

        # Row 1: Header (Trap Count label only)
        header = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(32), spacing=dp(4))
        self.count_label = MDLabel(text=f"{len(self.trap_list)} traps", size_hint_x=1.0, valign="center")
        self.count_label.bind(size=lambda s, w: setattr(s, 'text_size', w))

        header.add_widget(self.count_label)
        #left.add_widget(header)

        # Control panel: Manual mode on top, Time and Delay stacked below it
        controls = MDBoxLayout(orientation="vertical", size_hint_x=None, size_hint_y=None,
                               width=dp(230), height=dp(110), spacing=dp(6))

        # 1. Manual Mode Toggle Button row
        manual_row = MDBoxLayout(orientation="horizontal", size_hint_x=None, width=dp(230), size_hint_y=None,
                                 height=dp(32))
        self.manual_toggle_btn = MDButton(MDButtonText(text="Manual: Off"), style="filled", size_hint_x=None,
                                          width=dp(120), size_hint_y=None, height=dp(32))
        self.manual_toggle_btn.theme_bg_color = "Custom"
        self.manual_toggle_btn.md_bg_color = (0.2, 0.6, 0.2, 1)
        self.manual_toggle_btn.bind(on_release=lambda *_: self.toggle_manual_mode())
        manual_row.add_widget(self.manual_toggle_btn)

        # 2. Time Group: [Time Button] [Min Input] [Max Input]
        time_group = MDBoxLayout(orientation="horizontal", size_hint_x=None, width=dp(230), spacing=dp(6),
                                 size_hint_y=None, height=dp(32))
        time_apply_btn = MDButton(MDButtonText(text="Time"), style="filled", size_hint_x=None, width=dp(70),
                                  size_hint_y=None, height=dp(32))
        time_apply_btn.bind(on_release=lambda *_: self.apply_time())

        self.time_min_input = TextInput(text="10", multiline=False, size_hint_x=None, width=dp(74), size_hint_y=None,
                                        height=dp(32), font_size=dp(13), halign="center",
                                        background_color=(0.1, 0.1, 0.1, 1), foreground_color=(1, 1, 1, 1))
        self.time_max_input = TextInput(text="", hint_text="Max", multiline=False, size_hint_x=None, width=dp(74),
                                        size_hint_y=None, height=dp(32), font_size=dp(13), halign="center",
                                        background_color=(0.1, 0.1, 0.1, 1), foreground_color=(1, 1, 1, 1))

        time_group.add_widget(time_apply_btn)
        time_group.add_widget(self.time_min_input)
        time_group.add_widget(self.time_max_input)

        # 3. Delay Group: [Delay Button] [Delay Input]
        delay_group = MDBoxLayout(orientation="horizontal", size_hint_x=None, width=dp(230), spacing=dp(4),
                                  size_hint_y=None, height=dp(32))
        delay_apply_btn = MDButton(MDButtonText(text="Delay"), style="filled", size_hint_x=None, width=dp(70),
                                   size_hint_y=None, height=dp(32))
        delay_apply_btn.bind(on_release=lambda *_: self.apply_delayed_checks())

        self.delay_input = TextInput(text="3", multiline=False, size_hint_x=None, width=dp(74), size_hint_y=None,
                                     height=dp(32), font_size=dp(13), halign="center",
                                     background_color=(0.1, 0.1, 0.1, 1), foreground_color=(1, 1, 1, 1))

        delay_group.add_widget(delay_apply_btn)
        delay_group.add_widget(self.delay_input)

        controls.add_widget(manual_row)
        controls.add_widget(time_group)
        controls.add_widget(delay_group)
        left.add_widget(controls)

        # Scrollable grid layout for actual traps below controls
        self.grid = MDGridLayout(cols=1, size_hint_x=None, size_hint_y=None, spacing=dp(4), padding=dp(4))
        self.grid.bind(minimum_height=self.grid.setter("height"))

        scroll = MDScrollView(
            size_hint=(1, 1),
            bar_width=dp(10),
            bar_color=(1, 1, 1, 0.7),
            bar_inactive_color=(1, 1, 1, 0.3),
            scroll_type=["bars", "content"],
        )
        scroll.add_widget(self.grid)
        left.add_widget(scroll)

        self.add_widget(left)

        # --- right column: 50% width ---
        right = MDBoxLayout(orientation="vertical", size_hint_x=0.5, padding=(dp(8), 0, 0, 0))

        log_header = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(32), spacing=dp(4))
        log_label = MDLabel(text="Trap Log", size_hint_y=None, height=dp(24), valign="center")
        log_label.bind(size=lambda s, w: setattr(s, 'text_size', w))
        log_header.add_widget(log_label)
        right.add_widget(log_header)

        # Set up logger with timestamp formatter
        logger = logging.getLogger(log_logger_name)
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            formatter = logging.Formatter("[%(asctime)s] %(message)s", datefmt="%H:%M:%S")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        self.log_widget = UILog(logger)
        right.add_widget(self.log_widget)
        self.add_widget(right)

        self.populate(self.trap_list)

    @property
    def ctx(self):
        """Gets running app context."""
        return MDApp.get_running_app().ctx

    @mainthread
    def populate(self, trap_list):
        """Populates trap buttons."""
        self.grid.clear_widgets()
        self.trap_list = list(trap_list)
        self.count_label.text = f"{len(self.trap_list)} traps"

        logger = logging.getLogger("TrapSender")
        is_manual = getattr(self.ctx, "manual_mode", False)
        min_val = getattr(self.ctx, "time_min", 10)
        max_val = getattr(self.ctx, "time_max", None)
        delay_val = getattr(self.ctx, "delayed_start", 3)
        if getattr(self.ctx, "auth", None) is None:
            connectedmsg = f"Not connected! \nManual: {'On' if is_manual else 'Off'}\nTime: {min_val}-{max_val if max_val is not None else min_val}s\nDelay: {delay_val}"
        else:
            connectedmsg = f"Connected! (Loaded {len(self.trap_list)} traps) \nManual: {'On' if is_manual else 'Off'}\nTime: {min_val}-{max_val if max_val is not None else min_val}s\nDelay: {delay_val}"
        logger.info(connectedmsg)

        # Uniform button width based on the ACTUAL rendered pixel width of
        # the longest trap name (measured via Kivy's text engine), not a
        # char-count estimate -- proportional fonts render glyphs at
        # different widths, so counting characters doesn't line up evenly.
        if self.trap_list:
            max_text_width = max(_measure_text_width(t) for t in self.trap_list)
        else:
            max_text_width = dp(150)

        trap_btn_width = max_text_width + dp(70)  # horizontal padding inside the button, plus safety margin
        toggle_btn_width = dp(90)
        row_width = trap_btn_width + toggle_btn_width + dp(4)

        self.grid.width = row_width

        for trap_name in self.trap_list:
            is_blocked = trap_name in DISABLED_TRAPS

            # 1. Main trap trigger button
            btn = TrapButton(
                text=trap_name,
                size_hint_x=None,
                width=trap_btn_width,
                size_hint_y=None,
                height=dp(36)
            )
            btn.update_state(is_blocked)
            btn.bind(on_release=lambda inst, name=trap_name: self.send(name))

            # MDButton recalculates its own width when a child is added via
            # add_widget() after construction (which TrapButton does above),
            # silently overriding the explicit width we just set. Rather
            # than fight that internal behavior, wrap the button in a
            # fixed-width slot so the column stays aligned regardless of
            # whatever width MDButton decides to render itself at.
            btn_slot = AnchorLayout(
                size_hint_x=None, width=trap_btn_width,
                size_hint_y=None, height=dp(36),
                anchor_x="left", anchor_y="center",
            )
            btn_slot.add_widget(btn)

            # 2. Block/Allow toggle button with adaptive_width explicitly disabled
            toggle_text = MDButtonText(
                text="Off" if is_blocked else "On",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                adaptive_width=False,
                size_hint_x=1,
                size_hint_y=1
            )
            toggle_btn = MDButton(
                toggle_text,
                style="filled",
                size_hint_x=None,
                width=toggle_btn_width,
                size_hint_y=None,
                height=dp(36)
            )
            toggle_btn.theme_bg_color = "Custom"
            toggle_btn.text_widget = toggle_text

            if is_blocked:
                toggle_btn.md_bg_color = (0.8, 0.2, 0.2, 1)  # Red
            else:
                toggle_btn.md_bg_color = (0.2, 0.6, 0.2, 1)  # Green

            toggle_btn.bind(on_release=lambda inst, b_btn=btn, t_name=trap_name: self.toggle_trap(b_btn, inst, t_name))

            row = MDBoxLayout(
                orientation="horizontal",
                size_hint_x=None,
                width=row_width,
                size_hint_y=None,
                height=dp(36),
                spacing=dp(4)
            )
            row.add_widget(btn_slot)
            row.add_widget(toggle_btn)
            self.grid.add_widget(row)

    def toggle_trap(self, main_btn, toggle_btn, trap_name):
        """Toggles trap block status."""
        is_currently_blocked = trap_name in DISABLED_TRAPS

        if is_currently_blocked:
            set_trap_disabled(trap_name, False)
            main_btn.update_state(False)
            toggle_btn.text_widget.text = "On"
            toggle_btn.md_bg_color = (0.2, 0.6, 0.2, 1)
        else:
            set_trap_disabled(trap_name, True)
            main_btn.update_state(True)
            toggle_btn.text_widget.text = "Off"
            toggle_btn.md_bg_color = (0.8, 0.2, 0.2, 1)

    def toggle_manual_mode(self):
        """Toggles manual mode."""
        if hasattr(self.ctx, "manual_mode"):
            self.ctx.manual_mode = not self.ctx.manual_mode
            is_manual = self.ctx.manual_mode
            self.manual_toggle_btn.children[0].text = f"Manual: {'On' if is_manual else 'Off'}"
            self.manual_toggle_btn.md_bg_color = (0.8, 0.4, 0.1, 1) if is_manual else (0.2, 0.6, 0.2, 1)
            logging.getLogger("TrapSender").info(f"Set manual mode to {is_manual}")

    def apply_time(self):
        """Applies time settings."""
        if hasattr(self.ctx, "set_time"):
            try:
                min_val = float(self.time_min_input.text)
                max_text = self.time_max_input.text.strip()
                max_val = float(max_text) if max_text else None

                self.ctx.set_time(min_val, max_val)
                logging.getLogger("TrapSender").info(f"Updated time setting range to {min_val}-{max_val if max_val is not None else min_val}s")
            except ValueError:
                logging.getLogger("TrapSender").error("Invalid number format for time min/max settings.")

    def apply_delayed_checks(self):
        """Applies delayed check settings."""
        if hasattr(self.ctx, "set_delayedstart"):
            try:
                val = int(self.delay_input.text)
                self.ctx.set_delayedstart(val)
                logging.getLogger("TrapSender").info(f"Updated delayed checks setting to {val}")
            except ValueError:
                logging.getLogger("TrapSender").error("Invalid integer format for delayed checks setting.")

    def send(self, trap_name):
        """Sends a trap."""
        if trap_name in DISABLED_TRAPS:
            logging.getLogger("TrapSender").info(f"Blocked trap '{trap_name}' is disabled and cannot be sent.")
            return

        if hasattr(self.ctx, "cheat_item"):
            asyncio.create_task(self.ctx.cheat_item(trap_name))

    def send_all(self):
        """Sends all allowed traps."""
        for trap_name in self.trap_list:
            if trap_name not in DISABLED_TRAPS:
                self.send(trap_name)

    @mainthread
    def on_disconnect(self):
        """Resets panel on disconnect."""
        self.grid.clear_widgets()
        self.trap_list = []
        self.count_label.text = "0 traps"