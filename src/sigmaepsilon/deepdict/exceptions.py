class DeepDictLockedError(Exception):
    """
    Raised when a locked DeepDict is about to be modified.
    """

    def __init__(self, message="The object is locked!"):
        super().__init__(message)
