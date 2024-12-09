from tax import _
from tax.ui.ui_component_interface import UiComponentInterface
from tax.ui.ui_interface import UiInterface


class CliUi(UiInterface):
    title = _("Command line arguments")
    key = "cli"

    def collect_input(self, title: str = None, input_data: list[UiComponentInterface] = list) -> dict:
        response = {}
        for ui_component in input_data:
            response[ui_component.name] = ui_component.get_default_value()

        return response

    def output(self, title: str, data: list[tuple[str, str]]) -> None:
        print(f"{title}")
        for line in data:
            print(f"{line[0]} {line[1]}")
