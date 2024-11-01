from tax.calculators.calculator_interface import CalculatorInterface


class IkaCalculator(CalculatorInterface):

    def __init__(self, annual_gross_salary: float, salaries_count: float, kids_number: int):
        super().__init__(annual_gross_salary)
        self.salaries_count = salaries_count
        self.kids_number = kids_number

    def get_annual_insurance_cost(self) -> float:
        return 0

    def get_annual_tax(self) -> float:
        annual_taxable_income = self.annual_gross_salary - self.get_annual_insurance_cost()

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
        return (self.annual_gross_salary - annual_tax) / self.salaries_count

    def get_annual_net_salary(self) -> float:
        return self.annual_gross_salary - self.get_annual_tax()
