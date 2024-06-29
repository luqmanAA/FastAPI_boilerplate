
class ObjectDoesNotExist(Exception):
    """The requested object does not exist"""
    pass


class MultipleObjectsReturned(Exception):
    """The query returned multiple objects when only one was expected."""
    pass


class ObjectAlreadyExist(Exception):
    pass


class PageNotAnInteger(Exception):
    pass


class EmptyPage(Exception):
    pass


class ImageError(Exception):
    def __init__(self, message="A image error occurred."):
        self.message = message
        super().__init__(self.message)
