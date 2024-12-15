from abc import ABC, abstractmethod


class CalculatorInterface(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        pass

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
