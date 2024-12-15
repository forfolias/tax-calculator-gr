from tax.calculators.calculator_interface import CalculatorInterface


class BasicCalculator(CalculatorInterface):
    def __init__(self, annual_gross_salary: float = 0.0):
        self.annual_gross_salary = annual_gross_salary

    def get_annual_tax(self) -> float:
        return 0.0

    def get_annual_insurance_cost(self) -> float:
        return 0.0

    def get_monthly_net_salary(self) -> float:
        return self.get_annual_net_salary() / 12

    def get_annual_net_salary(self) -> float:
        annual_gross_salary = self.annual_gross_salary if self.annual_gross_salary is not None else 0
        return annual_gross_salary - self.get_annual_insurance_cost() - self.get_annual_tax()
