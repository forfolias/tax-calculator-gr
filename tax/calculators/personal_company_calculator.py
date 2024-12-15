from tax.calculators.basic_calculator import BasicCalculator
from tax.calculators.business_calculator_interface import BusinessCalculatorInterface
from tax.costs.company_health_insurance import CompanyHealthInsurance


class PersonalCompanyCalculator(BasicCalculator, BusinessCalculatorInterface):
    def __init__(self, annual_gross_salary: float = 0.0, monthly_insurance_cost: float = None, expenses: float = 0.0,
                 prepaid_tax: float = 0.0, functional_year: int = 0):
        super().__init__(annual_gross_salary)
        self.monthly_insurance_cost = monthly_insurance_cost if monthly_insurance_cost is not None else \
            CompanyHealthInsurance.costs[0].amount
        self.expenses = expenses
        self.prepaid_tax = prepaid_tax
        self.functional_year = functional_year

    def get_annual_insurance_cost(self) -> float:
        return self.monthly_insurance_cost * 12

    def get_tax_in_advance(self, annual_tax: float) -> float:
        return 0.0

    def get_gemi_cost(self) -> float:
        return 0.0
