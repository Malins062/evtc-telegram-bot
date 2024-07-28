import datetime as dt


def get_now(dt_format: str) -> str:
    """
    Return the current date and time in a specific format as a string

    :param dt_format:  Specific format datetime
    :return: Current date and time in a specific format as a string
    """

    now = dt.datetime.now()
    return now.strftime(dt_format)
