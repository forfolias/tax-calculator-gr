from tax.calculators.business_calculator_interface import BusinessCalculatorInterface
from tax.calculators.calculator_interface import CalculatorInterface
from tax.employment_types.employment_type import EmploymentTypeBase
from tax.costs.company_health_insurance import CompanyHealthInsurance
from tax.ui.interactive_shell_components import InputUiComponent, SelectOption, SelectUiComponent
from tax.ui.ui_interface import UiInterface


class PersonalCompanyEmploymentType(EmploymentTypeBase):
    title = ""
    calculator = None

    def __init__(self, ui: UiInterface, **kwargs):
        super().__init__(ui, **kwargs)

        self.annual_gross_salary = None
        if 'annual_gross_salary' in kwargs and kwargs['annual_gross_salary'] is not None:
            self.annual_gross_salary = kwargs['annual_gross_salary']

        self.monthly_insurance_cost = None
        if 'monthly_insurance_cost' in kwargs and kwargs['monthly_insurance_cost'] is not None:
            self.monthly_insurance_cost = kwargs['monthly_insurance_cost']

        self.expenses = None
        if 'expenses' in kwargs and kwargs['expenses'] is not None:
            self.expenses = kwargs['expenses']

        self.prepaid_tax = None
        if 'prepaid_tax' in kwargs and kwargs['prepaid_tax'] is not None:
            self.prepaid_tax = kwargs['prepaid_tax']

        self.functional_year = None
        if 'functional_year' in kwargs and kwargs['functional_year'] is not None:
            self.functional_year = kwargs['functional_year']

    def get_input_data(self) -> dict:
        input_data = super().get_input_data()
        insurance_classes = CompanyHealthInsurance.costs
        options = [SelectOption(f"{cost.title} ({cost.amount})", str(cost.amount)) for cost in insurance_classes]
        preselected_index = SelectUiComponent.get_index_of_option(
            options, self.monthly_insurance_cost
        ) if self.monthly_insurance_cost is not None else 0

        input_data['annual_gross_salary'] = InputUiComponent(
            label="Please enter your annual gross salary: ",
            placeholder=str(self.annual_gross_salary) if self.annual_gross_salary is not None else None,
            cast=float,
            validator=lambda count: count > 0
        )
        input_data['monthly_insurance_cost'] = SelectUiComponent(
            label="Please select the insurance class: ", cast=float,
            options=options,
            preselected_index=preselected_index
        )
        input_data['prepaid_tax'] = InputUiComponent(
            label="Please enter any prepaid tax amount from previous year: ", cast=float,
            placeholder=self.prepaid_tax if self.prepaid_tax is not None else "0",
            validator=lambda count: count >= 0
        )
        input_data['expenses'] = InputUiComponent(
            label="Please enter your annual expenses: ", cast=float,
            placeholder=self.expenses if self.expenses is not None else "0",
            validator=lambda count: count >= 0
        )
        input_data['functional_year'] = InputUiComponent(
            label="Please enter company's functional number of years: ", cast=int,
            placeholder=self.functional_year if self.functional_year is not None else "1",
            validator=lambda count: count >= 0)

        return input_data

    def get_output_data(self, calculator: BusinessCalculatorInterface) -> list[tuple[str, str]]:
        data = super().get_output_data(calculator)
        annual_tax = calculator.get_annual_tax()
        data.append(("Annual tax: ", f"{annual_tax:.2f}€"))
        data.append(("Annual insurance cost: ", f"{calculator.get_annual_insurance_cost():.2f}€"))
        data.append(("Tax in advance: ", f"{calculator.get_tax_in_advance(annual_tax):.2f}€"))

        return data
