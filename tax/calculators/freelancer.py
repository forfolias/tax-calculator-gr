from tax.calculators.calculator_interface import CalculatorInterface
from tax.insurance_classes.insurance_class import InsuranceClass


class FreelancerCalculator(CalculatorInterface):
    salaries_count = 12

    def __init__(self, annual_gross_salary: float, insurance_class: InsuranceClass, expenses: float):
        super().__init__(annual_gross_salary)
        self.insurance_class = insurance_class
        self.expenses = expenses

    def get_annual_insurance_cost(self) -> float:
        return self.insurance_class.cost * self.salaries_count

    def get_annual_tax(self):
        annual_taxable_income = self.annual_gross_salary - self.get_annual_insurance_cost() - self.expenses

        if annual_taxable_income <= 10000:
            tax = annual_taxable_income * 0.09
        elif annual_taxable_income <= 20000:
            tax = 10000 * 0.09 + (annual_taxable_income - 10000) * 0.22
        elif annual_taxable_income <= 30000:
            tax = 10000 * 0.09 + 10000 * 0.22 + (annual_taxable_income - 20000) * 0.28
        elif annual_taxable_income <= 40000:
            tax = 10000 * 0.09 + 10000 * 0.22 + 10000 * 0.28 + (annual_taxable_income - 30000) * 0.36
        else:
            tax = 10000 * 0.09 + 10000 * 0.22 + 10000 * 0.28 + 10000 * 0.36 + (annual_taxable_income - 40000) * 0.44

        return tax

    def get_monthly_net_salary(self) -> float:
        annual_tax = self.get_annual_tax()
        return (self.annual_gross_salary - self.expenses - annual_tax) / self.salaries_count

    def get_annual_net_salary(self) -> float:
        return self.annual_gross_salary - self.get_annual_tax()
