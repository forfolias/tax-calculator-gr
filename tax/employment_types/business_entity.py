from tax import _
from tax.costs.business_levy import BusynessLevy
from tax.employment_types.personal_company import PersonalCompanyEmploymentType
from tax.ui.interactive_shell_components import SelectOption, SelectUiComponent
from tax.ui.ui_interface import UiInterface


class BusinessEntityEmploymentType(PersonalCompanyEmploymentType):
    title = ""
    key = ""
    calculator = None

    def __init__(self, ui: UiInterface, **kwargs):
        super().__init__(ui, **kwargs)

        self.business_levy_cost = None
        if 'business_levy_cost' in kwargs and kwargs['business_levy_cost'] is not None:
            self.business_levy_cost = kwargs['business_levy_cost']

    def get_input_data(self) -> dict:
        input_data = super().get_input_data()

        options = [SelectOption(f"{cost.title} ({cost.amount})", str(cost.amount)) for cost in BusynessLevy.costs]
        preselected_index = SelectUiComponent.get_index_of_option(
            options, self.business_levy_cost
        ) if self.business_levy_cost is not None else 2
        input_data['business_levy_cost'] = SelectUiComponent(
            label=_("Business levy:"), cast=float,
            options=options,
            preselected_index=preselected_index
        )

        return input_data
