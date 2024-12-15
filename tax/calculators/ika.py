from tax.calculators.basic_calculator import BasicCalculator


class IkaCalculator(BasicCalculator):
    def __init__(self, annual_gross_salary: float = 0.0, salaries_count: float = 14.0, kids_number: int = 0):
        super().__init__(annual_gross_salary)
        self.salaries_count = salaries_count
        self.kids_number = kids_number

    def get_annual_insurance_cost(self) -> float:
        return self.annual_gross_salary * 0.13867

    def get_annual_tax(self) -> float:
        annual_taxable_income = self.annual_gross_salary - self.get_annual_insurance_cost()

        annual_discount = self._get_annual_tax_discount(annual_taxable_income)
        annual_tax = self.get_initial_annual_tax(annual_taxable_income)

        return annual_tax - annual_discount

    def get_monthly_net_salary(self) -> float:
        return self.get_annual_net_salary() / self.salaries_count

    def get_annual_net_salary(self) -> float:
        return self.annual_gross_salary - self.get_annual_insurance_cost() - self.get_annual_tax()

    @staticmethod
    def get_initial_annual_tax(annual_taxable_income):
        if annual_taxable_income <= 10000:
            return annual_taxable_income * 0.09
        elif annual_taxable_income <= 20000:
            return 10000 * 0.09 + (annual_taxable_income - 10000) * 0.22
        elif annual_taxable_income <= 30000:
            return 10000 * 0.09 + 10000 * 0.22 + (annual_taxable_income - 20000) * 0.28
        elif annual_taxable_income <= 40000:
            return 10000 * 0.09 + 10000 * 0.22 + 10000 * 0.28 + (annual_taxable_income - 30000) * 0.36
        else:
            return 10000 * 0.09 + 10000 * 0.22 + 10000 * 0.28 + 10000 * 0.36 + (annual_taxable_income - 40000) * 0.44

    def _get_annual_tax_discount(self, annual_taxable_income):
        if annual_taxable_income <= 12000:
            if self.kids_number == 0:
                return 777
            elif self.kids_number == 1:
                return 810
            elif self.kids_number == 2:
                return 900
            elif self.kids_number == 3:
                return 1120
            elif self.kids_number == 4:
                return 1340
            else:
                return 1340 + ((self.kids_number - 4) * 220)
        else:
            return self._get_discounted_annual_tax(annual_taxable_income)

    def _get_discounted_annual_tax(self, annual_taxable_income):
        discount = (annual_taxable_income - 12000) * 0.02
        if self.kids_number == 0:
            return 777 - discount
        elif self.kids_number == 1:
            return 810 - discount
        elif self.kids_number == 2:
            return 900 - discount
        elif self.kids_number == 3:
            return 1120 - discount
        elif self.kids_number == 4:
            return 1340 - discount
        else:
            return (1340 + ((self.kids_number - 4) * 220)) - discount
