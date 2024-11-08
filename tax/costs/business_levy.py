from tax.costs.cost_group import CostGroup
from tax.costs.cost import Cost


class BusynessLevy(CostGroup):
    title = "busyness levy"
    costs = (
        Cost("Category 1", 600),
        Cost("Category 2", 800),
        Cost("Category 3", 1000),
    )
