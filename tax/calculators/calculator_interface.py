from abc import ABC, abstractmethod


class CalculatorInterface(ABC):
    def __init__(self, annual_gross_salary: float):
        self.annual_gross_salary = annual_gross_salary

    @abstractmethod
    def get_annual_tax(self) -> float:
        pass

    @abstractmethod
    def get_annual_insurance_cost(self) -> float:
        pass

    @abstractmethod
    def get_monthly_net_salary(self) -> float:
        pass

    @abstractmethod
    def get_annual_net_salary(self) -> float:
        pass
