from tax.ui.apps.graphical_ui import GraphicalUi
from tax.ui.apps.interactive_shell_ui import InteractiveShellUi
from tax.ui.apps.cli_ui import CliUi

available_user_interfaces = (
    CliUi,
    InteractiveShellUi,
    GraphicalUi,
)
