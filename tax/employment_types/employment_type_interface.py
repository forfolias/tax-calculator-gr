from abc import ABC, abstractmethod

from tax.calculators.calculator_interface import CalculatorInterface


class EmploymentTypeInterface(ABC):
    title = None
    key = None
    calculator_class: type[CalculatorInterface]

    @abstractmethod
    def get_calculator(self) -> CalculatorInterface:
        pass
