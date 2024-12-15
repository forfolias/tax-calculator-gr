from tax import _
from tax.costs.cost_group import CostGroup
from tax.costs.cost import Cost


class BusinessLevy(CostGroup):
    title = _("business levy")
    costs = (
        Cost(_("category 1"), 600),
        Cost(_("category 2"), 800),
        Cost(_("category 3"), 1000),
    )
