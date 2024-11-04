from tax.calculators.calculator_interface import CalculatorInterface
from tax.insurance_classes.insurance_class import InsuranceClass


class FreelancerCalculator(CalculatorInterface):
    salaries_count = 12

    def __init__(self, annual_gross_salary: float, insurance_class: InsuranceClass, expenses: float, prepaid_tax: float,
                 functional_year: int):
        super().__init__(annual_gross_salary)
        self.insurance_class = insurance_class
        self.expenses = expenses
        self.prepaid_tax = prepaid_tax
        self.functional_year = functional_year

    def get_annual_insurance_cost(self) -> float:
        return self.insurance_class.cost * self.salaries_count

    def get_annual_tax(self):
        annual_taxable_income = self._get_annual_taxable_income()

        return self._get_initial_annual_tax(annual_taxable_income) - self.prepaid_tax

    def get_monthly_net_salary(self) -> float:
        return self.get_annual_net_salary() / self.salaries_count

    def get_annual_net_salary(self) -> float:
        annual_insurance_cost = self.get_annual_insurance_cost()
        annual_taxable_income = self._get_annual_taxable_income()
        initial_annual_tax = self._get_initial_annual_tax(annual_taxable_income)
        tax_in_advance = self._get_tax_in_advance(initial_annual_tax)

        return self.annual_gross_salary - initial_annual_tax - annual_insurance_cost - tax_in_advance - self.expenses

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

    def _get_tax_in_advance(self, annual_tax):
        if self.functional_year <= 3:
            return annual_tax * 0.55 * 0.5
        return annual_tax * 0.55
