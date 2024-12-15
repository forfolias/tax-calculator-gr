from typing import List

from beaupy import prompt, select, select_multiple
from rich import print

from tax import _
from tax.employment_types import available_employment_types
from tax.employment_types.employment_type import EmploymentTypeBase
from tax.ui.components.ui_component_interface import UiComponentInterface
from tax.ui.components.ui_components import InputUiComponent, SelectUiComponent
from tax.ui.apps.interactive_ui import InteractiveUI


class InteractiveShellUi(InteractiveUI):
    title = _("Interactive shell")
    key = "shell"

    def get_employment_types(self, **kwargs) -> List[EmploymentTypeBase]:
        print(_("Select employment type") + ":")
        indexes = select_multiple(
            options=[employment_type.title for employment_type in available_employment_types],
            minimal_count=1,
            ticked_indices=[0],
            return_indices=True,
        )
        return [available_employment_types[index](**kwargs) for index in indexes]

    def run(self) -> None:
        for employment_type in self.employment_types:
            input_data = employment_type.get_input_data()
            for ui_component in input_data:
                employment_type.parameters[ui_component.name] = self.render(ui_component)
            self.output(employment_type.title, employment_type.get_output_data())

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
            initial_value=str(ui_component.placeholder),
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
