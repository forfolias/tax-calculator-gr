from beaupy import prompt, select
from rich import print

from tax import _
from tax.ui.ui_component import UiComponent, InputTypes
from tax.ui.interactive_shell_components import InputUiComponent, SelectUiComponent
from tax.ui.ui_interface import UiInterface


class InteractiveShellUi(UiInterface):
    title = _("Interactive shell")
    key = "shell"

    def collect_input(self, input_data: dict[str, UiComponent]) -> dict:
        response = {}
        for element, ui_component in input_data.items():
            response[element] = self.render(ui_component)

        return response

    def output(self, title: str, data: list[tuple[str, str]]) -> None:
        print(f"[bold]{title}[/bold]")
        for line in data:
            print(f"{line[0]} [bold]{line[1]}[/bold]")

    def render(self, ui_component):
        if ui_component.input_type == InputTypes.Input:
            return self._render_input(ui_component)
        elif ui_component.input_type == InputTypes.Select:
            return self._render_select(ui_component)

    def _render_input(self, ui_component: InputUiComponent):
        return prompt(
            prompt=ui_component.label,
            target_type=ui_component.cast,
            initial_value=ui_component.placeholder,
            validator=ui_component.validator
        )

    def _render_select(self, ui_component: SelectUiComponent):
        print(ui_component.label)
        selected_index = select(
            options=[option.label for option in ui_component.options],
            cursor_index=ui_component.preselected_index,
            return_index=True
        )
        return ui_component.cast(ui_component.options[selected_index].value)
