from tax.costs.cost_group import CostGroup
from tax.costs.cost import Cost


class CompanyHealthInsurance(CostGroup):
    title = "EFKA"
    costs = (
        Cost("Category 1", 238.22),
        Cost("Category 2", 285.87),
        Cost("Category 3", 342.59),
        Cost("Category 4", 411.78),
        Cost("Category 5", 493.46),
        Cost("Category 6", 642.06),
        Cost("Special Category (<5 years)", 142.93),
    )
