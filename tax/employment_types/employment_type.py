from typing import Self

from tax import _
from tax.calculators.calculator_interface import CalculatorInterface
from tax.employment_types.employment_type_interface import EmploymentTypeInterface
from tax.exceptions import RequiredPropertyMissing
from tax.ui.ui_component import UiComponent
from tax.ui.ui_interface import UiInterface


class EmploymentTypeBase(EmploymentTypeInterface):
    protected_properties = ("title", "key", "calculator")

    def __init__(self, ui: UiInterface, **kwargs):
        self.ui = ui

    def input(self, **kwargs) -> Self:
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in self.protected_properties and getattr(self, key, None) is None:
                setattr(self, key, value)

        input_data = self.get_input_data()

        response = self.ui.collect_input(input_data=input_data)

        for element, value in response.items():
            setattr(self, element, value)

        return self

    def get_input_data(self) -> dict[str, UiComponent]:
        return {}

    def get_calculator(self) -> CalculatorInterface:
        calculator_properties = [
            k for k, v in self.calculator.__dict__.items()
            if not callable(v) and not k.startswith("__") and not k.startswith("_abc_")
        ]
        for calculator_property in calculator_properties:
            if not getattr(self, calculator_property):
                raise RequiredPropertyMissing(f"{calculator_property} is required")

        return self.get_calculator_instance()

    def get_calculator_instance(self) -> CalculatorInterface:
        return self.calculator()

    def output(self) -> None:
        calculator = self.get_calculator()
        data = self.get_output_data(calculator)
        self.ui.output(self.title, data)

    def get_output_data(self, calculator: CalculatorInterface) -> list[tuple[str, str]]:
        return [
            (_("Annual net income:"), f"{calculator.get_annual_net_salary():.2f}€"),
            (_("Monthly net income:"), f"{calculator.get_monthly_net_salary():.2f}€"),
        ]
