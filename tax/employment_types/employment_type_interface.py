from abc import ABC, abstractmethod

from tax.calculators.calculator_interface import CalculatorInterface


class EmploymentTypeInterface(ABC):

    title = None
    calculator = None

    @abstractmethod
    def get_calculator(self) -> CalculatorInterface:
        pass
