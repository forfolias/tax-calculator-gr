from tax import _
from tax.calculators.business_calculator_interface import BusinessCalculatorInterface
from tax.employment_types.employment_type import EmploymentTypeBase
from tax.costs.company_health_insurance import CompanyHealthInsurance
from tax.ui.ui_component_interface import UiComponentInterface
from tax.ui.ui_components import InputUiComponent, SelectOption, SelectUiComponent


class PersonalCompanyEmploymentType(EmploymentTypeBase):
    title = ""
    key = ""
    calculator = None

    @staticmethod
    def get_input_data(**kwargs) -> list[UiComponentInterface]:
        input_data = EmploymentTypeBase.get_input_data(**kwargs)
        insurance_classes = CompanyHealthInsurance.costs
        options = [SelectOption(f"{cost.title} ({cost.amount})", str(cost.amount)) for cost in insurance_classes]
        preselected_index = SelectUiComponent.get_index_of_option_value(
            options, kwargs['monthly_insurance_cost']
        ) if 'monthly_insurance_cost' in kwargs and kwargs['monthly_insurance_cost'] is not None else 0

        input_data.append(InputUiComponent(
            name='annual_gross_salary',
            label=_("annual gross salary"), cast=float,
            placeholder=str(kwargs['annual_gross_salary']) if 'annual_gross_salary' in kwargs and kwargs['annual_gross_salary'] is not None else None,
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
            placeholder=kwargs['prepaid_tax'] if 'prepaid_tax' in kwargs and kwargs['prepaid_tax'] is not None else "0",
            validator=lambda count: count >= 0
        ))
        input_data.append(InputUiComponent(
            name='expenses',
            label=_("annual expenses"), cast=float,
            placeholder=kwargs['expenses'] if 'expenses' in kwargs and kwargs['expenses'] is not None else "0",
            validator=lambda count: count >= 0
        ))
        input_data.append(InputUiComponent(
            name='functional_year',
            label=_("company's functional number of years"), cast=int,
            placeholder=kwargs['functional_year'] if 'functional_year' in kwargs and kwargs['functional_year'] is not None else "1",
            validator=lambda count: count >= 0
        ))

        return input_data

    def get_output_data(self, calculator: BusinessCalculatorInterface) -> list[tuple[str, str]]:
        data = super().get_output_data(calculator)
        annual_tax = calculator.get_annual_tax()
        data.append((_("annual tax"), f"{annual_tax:.2f}€"))
        data.append((_("annual insurance cost"), f"{calculator.get_annual_insurance_cost():.2f}€"))
        data.append((_("tax in advance"), f"{calculator.get_tax_in_advance(annual_tax):.2f}€"))

        return data
