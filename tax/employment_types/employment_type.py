from typing import Self

from tax.calculators.calculator_interface import CalculatorInterface
from tax.employment_types.employment_type_interface import EmploymentTypeInterface


class EmploymentTypeBase(EmploymentTypeInterface):
    protected_properties = ("title", "calculator")

    def input(self, **kwargs) -> Self:
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in self.protected_properties and getattr(self, key, None) is None:
                setattr(self, key, value)

        return self

    def get_calculator(self) -> CalculatorInterface:
        calculator_properties = [
            k for k, v in self.calculator.__dict__.items()
            if not callable(v) and not k.startswith("__") and not k.startswith("_abc_")
        ]
        for calculator_property in calculator_properties:
            if getattr(self, calculator_property) is None:
                raise Exception(f"{calculator_property} is required")

        return self.get_calculator_instance()

    def get_calculator_instance(self) -> CalculatorInterface:
        return self.calculator()
