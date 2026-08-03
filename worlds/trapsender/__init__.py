from worlds.LauncherComponents import Component, components, icon_paths, launch_subprocess, Type

def launch_client(*args):
    from .Client import launch
    from CommonClient import gui_enabled
    if not gui_enabled:
        print(args)
        launch(args)
    launch_subprocess(launch, name="Trap Sender Client", args=args)
components.append(Component("Trap Sender Client", "TrapSenderClient", func=launch_client,
                            component_type=Type.CLIENT, supports_uri=True, game_name=None))
