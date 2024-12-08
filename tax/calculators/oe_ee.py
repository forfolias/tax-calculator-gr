from tax.calculators.business_calculator_interface import BusinessCalculatorInterface


class OeEeCalculator(BusinessCalculatorInterface):
    annual_gross_salary = None
    monthly_insurance_cost = None
    expenses = None
    prepaid_tax = None
    functional_year = None
    business_levy_cost = None

    def __init__(self, annual_gross_salary: float, monthly_insurance_cost: float, expenses: float = 0,
                 prepaid_tax: float = 0, functional_year: int = 0, business_levy_cost: float = 0):
        super().__init__(annual_gross_salary)
        self.monthly_insurance_cost = monthly_insurance_cost
        self.expenses = expenses
        self.prepaid_tax = prepaid_tax
        self.functional_year = functional_year
        self.business_levy_cost = business_levy_cost

    def get_annual_insurance_cost(self) -> float:
        return self.monthly_insurance_cost * 12

    def get_annual_tax(self) -> float:
        annual_taxable_income = self.annual_gross_salary - self.expenses
        return annual_taxable_income * 0.22

    def get_monthly_net_salary(self) -> float:
        return self.get_annual_net_salary() / 12

    def get_annual_net_salary(self) -> float:
        annual_tax = self.get_annual_tax()
        tax_in_advance = self.get_tax_in_advance(annual_tax) - self.prepaid_tax
        standard_costs = self.get_annual_insurance_cost() + self.business_levy_cost + self.get_gemi_cost()
        return self.annual_gross_salary - annual_tax - tax_in_advance - standard_costs

    def get_tax_in_advance(self, annual_tax) -> float:
        if self.functional_year <= 3:
            return annual_tax * 0.4
        return annual_tax * 0.8

    def get_gemi_cost(self) -> float:
        return 80

    def get_statutory_reserve(self, profit) -> float:
        return profit * 0.05
