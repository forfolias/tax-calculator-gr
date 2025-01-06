import importlib.util

from tax.ui.apps.cli_ui import CliUi

available_user_interfaces = [CliUi]

if importlib.util.find_spec("beaupy") is not None:
    from tax.ui.apps.interactive_shell_ui import InteractiveShellUi
    available_user_interfaces.append(InteractiveShellUi)

if importlib.util.find_spec("tkinter") is not None:
    from tax.ui.apps.graphical_ui import GraphicalUi
    available_user_interfaces.append(GraphicalUi)

