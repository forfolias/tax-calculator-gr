class UnknownEmploymentType(Exception):
    pass


class UnknownUI(Exception):
    pass


class RequiredPropertyMissing(Exception):
    pass


class InvalidOption(Exception):
    def __init__(self, message):
        super().__init__(message)
