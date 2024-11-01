from tax.insurance_classes.insurance_class_group import InsuranceClassGroup
from tax.insurance_classes.insurance_class import InsuranceClass


class Freelancer(InsuranceClassGroup):
    title = "Freelancer"
    insurance_classes = (
        InsuranceClass("Category 1", 238.22),
        InsuranceClass("Category 2", 285.87),
        InsuranceClass("Category 3", 342.59),
        InsuranceClass("Category 4", 411.78),
        InsuranceClass("Category 5", 493.46),
        InsuranceClass("Category 6", 642.06),
        InsuranceClass("Special Category", 142.93),
    )
