from tax import _
from tax.costs.cost_group import CostGroup
from tax.costs.cost import Cost


class CompanyHealthInsurance(CostGroup):
    title = "EFKA"
    costs = (
        Cost(_("Category 1"), 238.22),
        Cost(_("Category 2"), 285.87),
        Cost(_("Category 3"), 342.59),
        Cost(_("Category 4"), 411.78),
        Cost(_("Category 5"), 493.46),
        Cost(_("Category 6"), 642.06),
        Cost(_("Special Category (<5 years)"), 142.93),
    )
