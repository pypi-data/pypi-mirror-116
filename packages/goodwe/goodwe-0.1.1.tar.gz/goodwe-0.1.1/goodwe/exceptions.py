class RequestFailedException(Exception):
    """Indicates requesting inverter data was unsuccessful"""


class InvalidDataException(Exception):
    """Indicates received data is invalid"""


class ProcessingException(Exception):
    """Indicates an error occurred during processing of inverter data"""


class MaxRetriesException(Exception):
    """Indicates the maximum number of retries has been reached"""
