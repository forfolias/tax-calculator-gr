from tax.employment_types.freelancer import FreelancerEmploymentType
from tax.employment_types.ika import IkaEmploymentType
from tax.employment_types.ike import IkeEmploymentType


available_employment_types = (
    ("ika", IkaEmploymentType),
    ("freelancer", FreelancerEmploymentType),
    ("ike", IkeEmploymentType),
)
