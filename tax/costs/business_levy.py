from tax import _
from tax.costs.cost_group import CostGroup
from tax.costs.cost import Cost


class BusynessLevy(CostGroup):
    title = "busyness levy"
    costs = (
        Cost(_("Category 1"), 600),
        Cost(_("Category 2"), 800),
        Cost(_("Category 3"), 1000),
    )
