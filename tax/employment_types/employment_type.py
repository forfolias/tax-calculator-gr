from inspect import signature

from tax import _
from tax.calculators.calculator_interface import CalculatorInterface
from tax.employment_types.employment_type_interface import EmploymentTypeInterface
from tax.exceptions import MissingValue
from tax.ui.components.ui_component_interface import UiComponentInterface


class EmploymentTypeBase(EmploymentTypeInterface):
    def __init__(self, **kwargs):
        self.parameters = {}
        params = signature(self.calculator_class.__init__).parameters
        for param_name, param in params.items():
            if param_name == "self":
                continue

            if param_name in kwargs and kwargs[param_name] is not None:
                self.parameters[param_name] = kwargs[param_name]
            else:
                self.parameters[param_name] = None

    def get_input_data(self) -> list[UiComponentInterface]:
        return []

    def validate_parameters(self) -> None:
        for param_name, param in self.parameters.items():
            if param is None:
                raise MissingValue(_("Missing value for '{name}'").format(name=param_name))

    def get_calculator(self) -> CalculatorInterface:
        self.validate_parameters()
        return self.calculator_class(**self.parameters)

    def get_output_data(self) -> list[tuple[str, str]]:
        calculator = self.get_calculator()
        return [
            (_("annual net income"), f"{calculator.get_annual_net_salary():.2f}€"),
            (_("monthly net income"), f"{calculator.get_monthly_net_salary():.2f}€"),
        ]
