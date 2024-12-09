from beaupy import prompt, select
from rich import print

from tax import _
from tax.ui.ui_component_interface import UiComponentInterface, InputTypes
from tax.ui.ui_components import InputUiComponent, SelectUiComponent
from tax.ui.ui_interface import UiInterface


class InteractiveShellUi(UiInterface):
    title = _("Interactive shell")
    key = "shell"

    def collect_input(self, title: str = None, input_data: list[UiComponentInterface] = list) -> dict:
        response = {}
        print(title)
        for ui_component in input_data:
            response[ui_component.name] = self.render(ui_component)

        return response

    def output(self, title: str, data: list[tuple[str, str]]) -> None:
        print(f"[bold]{title}[/bold]")
        for line in data:
            print(f"{line[0]} [bold]{line[1]}[/bold]")

    def render(self, ui_component: UiComponentInterface):
        if isinstance(ui_component, InputUiComponent):
            return self._render_input(ui_component)
        elif isinstance(ui_component, SelectUiComponent):
            return self._render_select(ui_component)

    def _render_input(self, ui_component: InputUiComponent):
        return prompt(
            prompt=ui_component.label.capitalize() + ":",
            target_type=ui_component.cast,
            initial_value=ui_component.placeholder,
            validator=ui_component.validator
        )

    def _render_select(self, ui_component: SelectUiComponent):
        print(ui_component.label.capitalize() + ":")
        selected_index = select(
            options=[option.label for option in ui_component.options],
            cursor_index=ui_component.preselected_index,
            return_index=True
        )
        return ui_component.cast(ui_component.options[selected_index].value)
