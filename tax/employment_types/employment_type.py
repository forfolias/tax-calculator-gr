from tax import _
from tax.calculators.calculator_interface import CalculatorInterface
from tax.employment_types.employment_type_interface import EmploymentTypeInterface
from tax.exceptions import MissingValue
from tax.ui.ui_component_interface import UiComponentInterface
from tax.ui.ui_interface import UiInterface


class EmploymentTypeBase(EmploymentTypeInterface):

    def __init__(self, ui: UiInterface):
        self.ui = ui

    def run(self, **kwargs):
        input_data = self.get_input_data(**kwargs)

        response = self.ui.collect_input(title=self.title, input_data=input_data)

        for key, value in response.items():
            if value is None:
                label = next((ui.label for ui in input_data if key == ui.name), key)
                raise MissingValue(_("Missing value for '{name}'").format(name=label))

        calculator = self.get_calculator(**response)
        output_data = self.get_output_data(calculator)
        self.ui.output(self.title, output_data)

    @staticmethod
    def get_input_data(**kwargs) -> list[UiComponentInterface]:
        return []

    def get_calculator(self, **kwargs) -> CalculatorInterface:
        return self.calculator(**kwargs)

    def get_output_data(self, calculator: CalculatorInterface) -> list[tuple[str, str]]:
        return [
            (_("annual net income"), f"{calculator.get_annual_net_salary():.2f}€"),
            (_("monthly net income"), f"{calculator.get_monthly_net_salary():.2f}€"),
        ]
