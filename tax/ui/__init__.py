from tax.ui.graphical_ui import GraphicalUi
from tax.ui.interactive_shell_ui import InteractiveShellUi
from tax.ui.cli_ui import CliUi

available_user_interfaces = (
    CliUi,
    InteractiveShellUi,
    GraphicalUi,
)
