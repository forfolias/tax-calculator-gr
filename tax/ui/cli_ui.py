from tax.ui.ui_component import UiComponent
from tax.ui.ui_interface import UiInterface


class CliUi(UiInterface):
    title = "Command line arguments"
    key = "cli"

    def collect_input(self, input_data: dict[str, UiComponent]) -> dict:
        response = {}
        for element, ui_component in input_data.items():
            response[element] = ui_component.get_default_value()

        return response

    def output(self, title: str, data: list[tuple[str, str]]) -> None:
        print(f"{title}")
        for line in data:
            print(f"{line[0]}{line[1]}")
