from tax.employment_types.freelancer import FreelancerEmploymentType
from tax.employment_types.ika import IkaEmploymentType
from tax.employment_types.ike import IkeEmploymentType
from tax.employment_types.oe_ee import OeEeEmploymentType

available_employment_types = (
    IkaEmploymentType,
    FreelancerEmploymentType,
    IkeEmploymentType,
    OeEeEmploymentType,
)
