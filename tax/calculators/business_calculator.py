from tax.calculators.personal_company_calculator import PersonalCompanyCalculator
from tax.costs.business_levy import BusinessLevy


class BusinessCalculator(PersonalCompanyCalculator):

    def __init__(self, annual_gross_salary: float = 0.0, monthly_insurance_cost: float = None, expenses: float = 0.0,
                 prepaid_tax: float = 0.0, functional_year: int = 0, business_levy_cost: float = None):
        super().__init__(annual_gross_salary, monthly_insurance_cost, expenses, prepaid_tax, functional_year)
        self.business_levy_cost = business_levy_cost if business_levy_cost is not None else BusinessLevy.costs[1].amount

    def get_annual_tax(self) -> float:
        annual_taxable_income = self.annual_gross_salary - self.expenses
        return annual_taxable_income * 0.22
