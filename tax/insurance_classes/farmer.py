from tax.insurance_classes.insurance_class_group import InsuranceClassGroup
from tax.insurance_classes.insurance_class import InsuranceClass


class Farmer(InsuranceClassGroup):
    title = "Farmer"
    insurance_classes = (
        InsuranceClass("TBD", 0),
    )
