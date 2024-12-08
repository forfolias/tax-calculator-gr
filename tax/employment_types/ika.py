from tax import _
from tax.calculators.calculator_interface import CalculatorInterface
from tax.calculators.ika import IkaCalculator
from tax.employment_types.employment_type import EmploymentTypeBase
from tax.ui.ui_component import UiComponent
from tax.ui.interactive_shell_components import InputUiComponent, SelectOption, SelectUiComponent
from tax.ui.ui_interface import UiInterface


class IkaEmploymentType(EmploymentTypeBase):
    title = _("IKA")
    key = "ika"
    calculator = IkaCalculator
    annual_gross_salary = None
    salaries_count = None
    kids_number = 0

    def __init__(self, ui: UiInterface, **kwargs):
        super().__init__(ui, **kwargs)

        self.annual_gross_salary = None
        if 'annual_gross_salary' in kwargs and kwargs['annual_gross_salary'] is not None:
            self.annual_gross_salary = kwargs['annual_gross_salary']

        self.salaries_count = None
        if 'salaries_count' in kwargs and kwargs['salaries_count']:
            self.salaries_count = kwargs['salaries_count']

        self.kids_number = None
        if 'kids_number' in kwargs and kwargs['kids_number'] is not None:
            self.kids_number = kwargs['kids_number']

    def get_input_data(self) -> dict[str, UiComponent]:
        input_data = super().get_input_data()

        input_data['annual_gross_salary'] = InputUiComponent(
            label=_("Annual gross salary:"),
            placeholder=self.annual_gross_salary if self.annual_gross_salary is not None else "",
            cast=float,
            validator=lambda count: count > 0
        )

        options = [SelectOption("12", "12"), SelectOption("14", "14"), SelectOption("14.5", "14.5")]
        preselected_index = SelectUiComponent.get_index_of_option(
            options,
            self.salaries_count
        ) if self.salaries_count is not None else 1
        input_data['salaries_count'] = SelectUiComponent(
            label=_("Number of annual salaries:"), cast=float,
            options=options,
            preselected_index=preselected_index
        )

        input_data['kids_number'] = InputUiComponent(
            label=_("Number of kids:"),
            placeholder=str(self.kids_number) if self.kids_number is not None else "0",
            cast=int,
            validator=lambda count: count >= 0
        )

        return input_data

    def get_calculator_instance(self) -> CalculatorInterface:
        return self.calculator(
            annual_gross_salary=float(self.annual_gross_salary),
            salaries_count=float(self.salaries_count),
            kids_number=int(self.kids_number),
        )
