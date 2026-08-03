"""
Traps tab widget (kivymd-based) for TrapSenderContext.

IMPORTANT: this module imports kivymd, which imports kivy, at module level.
kvui.py requires that IT be the first thing to import kivy (it sets DPI /
env-var config before kivy's window subsystem initializes -- see the
assert at the top of kvui.py). That means this module must NOT be imported
at the top of Client.py. Import it lazily, inside make_gui(), AFTER
super().make_gui() has already triggered kvui's import. See
TrapSenderClient.py for the exact pattern.

Plain extraction logic that has no kivy dependency lives in trap_utils.py
instead, and is safe to import normally.
"""

from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
import asyncio


class TrapPanel(MDBoxLayout):
    """
    Content widget for the "Traps" tab. Starts empty -- call
    trap_panel.populate(get_trap_names(world)) once the tracker's world is
    actually loaded (see populate_trap_tab() in TrapSenderClient.py).
    """

    def __init__(self, trap_list=None, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.trap_list = trap_list or []

        header = MDBoxLayout(size_hint_y=None, height=dp(40), padding=dp(4), spacing=dp(4))
        self.count_label = MDLabel(text=f"{len(self.trap_list)} traps")
        send_all_btn = MDButton(MDButtonText(text="Send All"), style="filled",
                                 size_hint_x=None, width=dp(120))
        send_all_btn.bind(on_release=lambda *_: self.send_all())
        header.add_widget(self.count_label)
        header.add_widget(send_all_btn)
        self.add_widget(header)

        self.grid = MDGridLayout(cols=1, size_hint_y=None, spacing=dp(4), padding=dp(4))
        self.grid.bind(minimum_height=self.grid.setter("height"))

        scroll = MDScrollView(size_hint=(1, 1))
        scroll.add_widget(self.grid)
        self.add_widget(scroll)

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
            btn = MDButton(MDButtonText(text=trap_name), style="outlined",
                            size_hint_y=None, height=dp(36))
            btn.bind(on_release=lambda inst, name=trap_name: self.send(name))
            self.grid.add_widget(btn)

    def send(self, trap_name):
        """Reuses your existing cheat_item() coroutine -- the real send path."""
        asyncio.create_task(self.ctx.cheat_item(trap_name))

    def send_all(self):
        for trap_name in self.trap_list:
            self.send(trap_name)