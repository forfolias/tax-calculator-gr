from typing import Self


from tax.costs.business_levy import BusynessLevy
from tax.employment_types.personal_company import PersonalCompanyEmploymentType


class BusinessEntityEmploymentType(PersonalCompanyEmploymentType):
    title = ""
    calculator = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.business_levy_cost = None
        if 'business_levy_cost' in kwargs and kwargs['business_levy_cost'] is not None:
            self.business_levy_cost = float(kwargs['business_levy_cost'])

    def input(self, **kwargs) -> Self:
        super().input(**kwargs)

        from beaupy import select

        busyness_levies = BusynessLevy.costs
        if not self.business_levy_cost:
            print("Please select the business levy:")
            index = select(
                options=busyness_levies,
                preprocessor=lambda cost: f"{cost.title} ({cost.amount})",
                cursor_index=2,
                return_index=True
            )
            self.business_levy_cost = busyness_levies[index].amount
        elif isinstance(self.business_levy_cost, (int,)):
            self.business_levy_cost = busyness_levies[int(self.business_levy_cost)].amount
        elif isinstance(self.business_levy_cost, (str,)):
            self.business_levy_cost = float(self.business_levy_cost)

        return self
