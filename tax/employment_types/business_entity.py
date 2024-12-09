from tax import _
from tax.costs.business_levy import BusynessLevy
from tax.employment_types.personal_company import PersonalCompanyEmploymentType
from tax.ui.ui_component_interface import UiComponentInterface
from tax.ui.ui_components import SelectOption, SelectUiComponent


class BusinessEntityEmploymentType(PersonalCompanyEmploymentType):
    title = None
    key = None
    calculator = None

    @staticmethod
    def get_input_data(**kwargs) -> list[UiComponentInterface]:
        input_data = PersonalCompanyEmploymentType.get_input_data(**kwargs)

        options = [SelectOption(f"{cost.title} ({cost.amount})", str(cost.amount)) for cost in BusynessLevy.costs]
        preselected_index = SelectUiComponent.get_index_of_option_value(
            options, kwargs['business_levy_cost']
        ) if 'business_levy_cost' in kwargs and kwargs['business_levy_cost'] is not None else 2
        input_data.append(SelectUiComponent(
            name='business_levy_cost',
            label=_("business levy"), cast=float,
            options=options,
            preselected_index=preselected_index
        ))

        return input_data
