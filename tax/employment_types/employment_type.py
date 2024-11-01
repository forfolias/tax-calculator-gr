from tax.calculators.calculator_interface import CalculatorInterface
from tax.employment_types.employment_type_interface import EmploymentTypeInterface


class EmploymentTypeBase(EmploymentTypeInterface):
    protected_properties = ("title", "calculator")

    def input(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in self.protected_properties:
                setattr(self, key, value)

    def get_calculator(self) -> CalculatorInterface:
        return self.calculator()
