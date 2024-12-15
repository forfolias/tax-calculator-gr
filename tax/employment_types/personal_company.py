from tax import _
from tax.calculators.business_calculator_interface import BusinessCalculatorInterface
from tax.employment_types.employment_type import EmploymentTypeBase
from tax.costs.company_health_insurance import CompanyHealthInsurance
from tax.ui.components.ui_component_interface import UiComponentInterface
from tax.ui.components.ui_components import InputUiComponent, SelectOption, SelectUiComponent


class PersonalCompanyEmploymentType(EmploymentTypeBase):
    title = ""
    key = ""
    calculator_class: type[BusinessCalculatorInterface]

    def get_input_data(self) -> list[UiComponentInterface]:
        input_data = super().get_input_data()
        insurance_classes = CompanyHealthInsurance.costs
        options = [SelectOption(f"{cost.title} ({cost.amount}€)", str(cost.amount)) for cost in insurance_classes]
        preselected_index = SelectUiComponent.get_index_of_option_value(
            options, str(self.parameters['monthly_insurance_cost'])
        ) if 'monthly_insurance_cost' in self.parameters and self.parameters['monthly_insurance_cost'] is not None else 0

        input_data.append(InputUiComponent(
            name='annual_gross_salary',
            label=_("annual gross salary"), cast=float,
            placeholder=str(self.parameters['annual_gross_salary']) if 'annual_gross_salary' in self.parameters and self.parameters['annual_gross_salary'] is not None else "",
            validator=lambda count: count > 0
        ))
        input_data.append(SelectUiComponent(
            name='monthly_insurance_cost',
            label=_("insurance class"), cast=float,
            options=options,
            preselected_index=preselected_index
        ))
        input_data.append(InputUiComponent(
            name='prepaid_tax',
            label=_("prepaid tax amount from previous year"), cast=float,
            placeholder=self.parameters['prepaid_tax'] if 'prepaid_tax' in self.parameters and self.parameters['prepaid_tax'] is not None else "0",
            validator=lambda count: count >= 0
        ))
        input_data.append(InputUiComponent(
            name='expenses',
            label=_("annual expenses"), cast=float,
            placeholder=self.parameters['expenses'] if 'expenses' in self.parameters and self.parameters['expenses'] is not None else "0",
            validator=lambda count: count >= 0
        ))
        input_data.append(InputUiComponent(
            name='functional_year',
            label=_("company's functional number of years"), cast=int,
            placeholder=self.parameters['functional_year'] if 'functional_year' in self.parameters and self.parameters['functional_year'] is not None else "1",
            validator=lambda count: count >= 0
        ))

        return input_data

    def get_calculator(self) -> BusinessCalculatorInterface:
        self.validate_parameters()
        return self.get_calculator_instance()

    def get_calculator_instance(self) -> BusinessCalculatorInterface:
        return self.calculator_class(**self.parameters)

    def get_output_data(self) -> list[tuple[str, str]]:
        data = super().get_output_data()
        calculator = self.get_calculator()
        annual_tax = calculator.get_annual_tax()
        data.append((_("annual tax"), f"{annual_tax:.2f}€"))
        data.append((_("annual insurance cost"), f"{calculator.get_annual_insurance_cost():.2f}€"))
        data.append((_("tax in advance"), f"{calculator.get_tax_in_advance(annual_tax):.2f}€"))

        return data
