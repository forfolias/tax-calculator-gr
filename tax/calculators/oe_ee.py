from tax.calculators.business_calculator import BusinessCalculator


class OeEeCalculator(BusinessCalculator):

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
