from tax.calculators.business_calculator import BusinessCalculator
from tax.costs.business_levy import BusinessLevy


class IkeCalculator(BusinessCalculator):

    def __init__(self, annual_gross_salary: float = 0.0, monthly_insurance_cost: float = None, expenses: float = 0.0,
                 prepaid_tax: float = 0.0, functional_year: int = 0, business_levy_cost: float = None, has_statutory_reserve: bool = False):
        business_levy_cost = business_levy_cost if business_levy_cost is not None else BusinessLevy.costs[2].amount
        super().__init__(annual_gross_salary, monthly_insurance_cost, expenses, prepaid_tax, functional_year, business_levy_cost)
        self.has_statutory_reserve = has_statutory_reserve

    def get_annual_net_salary(self) -> float:
        annual_tax = self.get_annual_tax()
        tax_in_advance = self.get_tax_in_advance(annual_tax) - self.prepaid_tax
        statutory_reserve = self.get_statutory_reserve(self.annual_gross_salary - (annual_tax + tax_in_advance))
        annual_undistributed_profit = self.annual_gross_salary - annual_tax - tax_in_advance - statutory_reserve
        annual_distribution_cost = self.get_dividend_tax(annual_undistributed_profit)
        standard_costs = self.get_annual_insurance_cost() + self.business_levy_cost + self.get_gemi_cost()
        return annual_undistributed_profit - annual_distribution_cost - standard_costs

    def get_tax_in_advance(self, annual_tax) -> float:
        if self.functional_year <= 1:
            return annual_tax * 0.5
        return annual_tax * 0.8

    def get_gemi_cost(self) -> float:
        return 100

    @staticmethod
    def get_dividend_tax(annual_profit) -> float:
        return annual_profit * 0.05

    def get_statutory_reserve(self, profit) -> float:
        return profit * 0.05 if self.has_statutory_reserve else 0.0
