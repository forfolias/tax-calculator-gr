from abc import ABC, abstractmethod

from tax.calculators.calculator_interface import CalculatorInterface


class BusinessCalculatorInterface(CalculatorInterface, ABC):

    @abstractmethod
    def get_tax_in_advance(self, annual_tax: float) -> float:
        pass

    @abstractmethod
    def get_gemi_cost(self) -> float:
        pass
