from tax import _
from tax.costs.cost_group import CostGroup
from tax.costs.cost import Cost


class CompanyHealthInsurance(CostGroup):
    title = "EFKA"
    costs = (
        Cost(_("category 1"), 238.22),
        Cost(_("category 2"), 285.87),
        Cost(_("category 3"), 342.59),
        Cost(_("category 4"), 411.78),
        Cost(_("category 5"), 493.46),
        Cost(_("category 6"), 642.06),
        Cost(_("special category (<5 years)"), 142.93),
    )
