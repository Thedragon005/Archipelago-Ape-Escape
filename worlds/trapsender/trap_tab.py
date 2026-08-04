"""
Traps tab widget (kivymd-based) for TrapSenderContext.

IMPORTANT: this module imports kivy/kivymd/kvui at module level, so it must
only ever be imported lazily, from inside make_gui() -- AFTER
super().make_gui() has already caused kvui to load kivy first. See
TrapSenderClient.py's make_gui() for the exact pattern. Never import this
module at the top of Client.py.
"""

import logging
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kvui import HoverBehavior, UILog
import asyncio


class TrapButton(HoverBehavior, MDButton):
    """
    MDButton's own hover state layer can be unreliable depending on
    kivymd/theme setup. This sidesteps it with an explicit background swap
    on enter/leave, using the same HoverBehavior mixin kvui.py's own
    HovererableLabel/ServerLabel already use.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.theme_bg_color == "Primary":
            self.theme_bg_color = "Custom"
        self.md_bg_color = self.theme_cls.surfaceContainerLowColor

    def on_enter(self):
        self.md_bg_color = self.theme_cls.primaryContainerColor

    def on_leave(self):
        self.md_bg_color = self.theme_cls.surfaceContainerLowColor


class TrapPanel(MDBoxLayout):
    """
    Content widget for the "Traps" tab: a scrollable button grid on the
    left, and a live log panel on the right bound to logging.getLogger
    ("TrapSender") -- so anything routed through that logger (see
    Client.py's trap_logger) shows up here in place, without needing its
    own tab.
    """

    def __init__(self, trap_list=None, log_logger_name="TrapSender", **kwargs):
        super().__init__(orientation="horizontal", **kwargs)
        self.trap_list = trap_list or []

        # --- left column: header + scrollable button grid ---
        left = MDBoxLayout(orientation="vertical", size_hint_x=0.65)

        header = MDBoxLayout(size_hint_y=None, height=dp(40), padding=dp(4), spacing=dp(4))
        self.count_label = MDLabel(text=f"{len(self.trap_list)} traps")
        send_all_btn = MDButton(MDButtonText(text="Send All"), style="filled",
                                 size_hint_x=None, width=dp(120))
        send_all_btn.bind(on_release=lambda *_: self.send_all())
        header.add_widget(self.count_label)
        header.add_widget(send_all_btn)
        left.add_widget(header)

        self.grid = MDGridLayout(cols=1, size_hint_y=None, spacing=dp(4), padding=dp(4))
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

        # --- right column: TrapSender-only log panel ---
        right = MDBoxLayout(orientation="vertical", size_hint_x=0.35, padding=(dp(8), 0, 0, 0))
        right.add_widget(MDLabel(text="Trap Log", size_hint_y=None, height=dp(30)))
        right.add_widget(UILog(logging.getLogger(log_logger_name)))
        self.add_widget(right)

        self.populate(self.trap_list)

    @property
    def ctx(self):
        """Same pattern kvui.py's own ServerLabel uses to reach ctx."""
        return MDApp.get_running_app().ctx

    def populate(self, trap_list):
        """(Re)build the buttons -- called once the world/trap list is known."""
        self.grid.clear_widgets()
        self.trap_list = list(trap_list)
        self.count_label.text = f"{len(self.trap_list)} traps"

        for trap_name in self.trap_list:
            # Replaced TrapButton with standard MDButton for testing
            btn = MDButton(
                MDButtonText(text=trap_name),
                style="filled",        # Changed from "outlined"
                size_hint_x=1,         # Forces button to fill the width
                size_hint_y=None,
                height=dp(36)
            )
            btn.bind(on_release=lambda inst, name=trap_name: self.send(name))
            self.grid.add_widget(btn)

    def send(self, trap_name):
        """Reuses your existing cheat_item() coroutine -- the real send path."""
        asyncio.create_task(self.ctx.cheat_item(trap_name))

    def send_all(self):
        for trap_name in self.trap_list:
            self.send(trap_name)