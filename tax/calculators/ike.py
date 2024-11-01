from tax.calculators.calculator_interface import CalculatorInterface
from tax.insurance_classes.insurance_class import InsuranceClass


class IkeCalculator(CalculatorInterface):
    tax_percentage = 0.22
    salaries_count = 12

    def __init__(self, annual_gross_salary: float, insurance_class: InsuranceClass, expenses: float):
        super().__init__(annual_gross_salary)
        self.insurance_class = insurance_class
        self.expenses = expenses

    def get_annual_insurance_cost(self) -> float:
        return self.insurance_class.cost * self.salaries_count

    def get_annual_tax(self) -> float:
        annual_taxable_income = self.annual_gross_salary - self.get_annual_insurance_cost() - self.expenses
        return annual_taxable_income*self.tax_percentage

    def get_monthly_net_salary(self) -> float:
        annual_tax = self.get_annual_tax()
        return (self.annual_gross_salary - self.expenses - annual_tax) / self.salaries_count

    def get_annual_net_salary(self) -> float:
        return self.annual_gross_salary - self.get_annual_tax()
