class InvalidHeaderError(Exception):
    """Raised when a header element contains invalid data."""
    def __init__(self, header_element: str, *args: object) -> None:
        message = f"Header element '{header_element}' contains invalid data."
        super().__init__(message, *args)
