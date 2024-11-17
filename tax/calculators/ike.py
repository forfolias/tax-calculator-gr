from tax.calculators.calculator_interface import CalculatorInterface


class IkeCalculator(CalculatorInterface):
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
        tax_in_advance = self._get_tax_in_advance(annual_tax) - self.prepaid_tax
        statutory_reserve = self._get_statutory_reserve(self.annual_gross_salary - (annual_tax + tax_in_advance))
        annual_undistributed_profit = self.annual_gross_salary - annual_tax - tax_in_advance - statutory_reserve
        annual_distribution_cost = self._get_dividend_tax(annual_undistributed_profit)
        standard_costs = self.get_annual_insurance_cost() + self._get_gemi_cost() + self.business_levy_cost
        return annual_undistributed_profit - annual_distribution_cost - standard_costs

    def _get_tax_in_advance(self, annual_tax) -> float:
        if self.functional_year <= 1:
            return annual_tax * 0.5
        return annual_tax * 0.8

    def _get_gemi_cost(self) -> float:
        return 100

    def _get_dividend_tax(self, annual_profit) -> float:
        return annual_profit * 0.05

    def _get_statutory_reserve(self, profit) -> float:
        return profit * 0.05
