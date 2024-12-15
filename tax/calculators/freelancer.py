from tax.calculators.personal_company_calculator import PersonalCompanyCalculator


class FreelancerCalculator(PersonalCompanyCalculator):

    def get_annual_tax(self):
        annual_taxable_income = self._get_annual_taxable_income()

        return self._get_initial_annual_tax(annual_taxable_income) - self.prepaid_tax

    def get_annual_net_salary(self) -> float:
        annual_taxable_income = self._get_annual_taxable_income()
        initial_annual_tax = self._get_initial_annual_tax(annual_taxable_income)
        tax_in_advance = self.get_tax_in_advance(initial_annual_tax)
        standard_costs = self.get_annual_insurance_cost() + self.get_gemi_cost()
        return self.annual_gross_salary - initial_annual_tax - standard_costs - tax_in_advance - self.expenses

    def get_tax_in_advance(self, annual_tax) -> float:
        if self.functional_year <= 3:
            return annual_tax * 0.55 * 0.5
        return annual_tax * 0.55

    def get_gemi_cost(self) -> float:
        return 45

    def _get_annual_taxable_income(self) -> float:
        return self.annual_gross_salary - self.get_annual_insurance_cost() - self.expenses

    def _get_initial_annual_tax(self, annual_taxable_income) -> float:
        if annual_taxable_income <= 10000:
            if self.functional_year <= 3:
                return annual_taxable_income * 0.045
            else:
                return annual_taxable_income * 0.09
        elif annual_taxable_income <= 20000:
            return 10000 * 0.09 + (annual_taxable_income - 10000) * 0.22
        elif annual_taxable_income <= 30000:
            return 10000 * 0.09 + 10000 * 0.22 + (annual_taxable_income - 20000) * 0.28
        elif annual_taxable_income <= 40000:
            return 10000 * 0.09 + 10000 * 0.22 + 10000 * 0.28 + (annual_taxable_income - 30000) * 0.36
        else:
            return 10000 * 0.09 + 10000 * 0.22 + 10000 * 0.28 + 10000 * 0.36 + (annual_taxable_income - 40000) * 0.44
