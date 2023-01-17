class Error(Exception):
    """Base class for exceptions in this module.

    attributes:
        expected: the expected value or range of values
        actual: the actual value
        message_head: a header format that references the error class (str)
        message_tail: a footer format that references the expected and actual values (str)
    """

    def __init__(self):
        self.expected = None
        self.actual = None
        self.message_head = f"Error: {self.__class__.__name__}"
        self.message_tail = f"\n\t- Expected: {self.expected}\n\t- Received: {self.actual}."

    def generate_error_message(self):
        """Generates an error message for the exception.

        returns:
            message: the error message (str)
        """
        message = self.message_head + self.message_tail
        return


class KeySizeError(Error):
    """Exception raised for errors in the key size.

    attributes:
        expected: a string for the number of characters expected
        actual: the received value
    """

    def __init__(self, actual: str):
        self.expected = "64 characters"
        self.actual = actual
        super().__init__()


class NodeKeyDoesNotExistError(Error):
    """Exception raised for errors in the key size.

    attributes:
        expected: the expected value or range of values (str)
        actual: the actual value (str)
    """

    def __init__(self, actual: str):
        self.expected = "A node object associated with the key"
        self.actual = actual
        super().__init__()
