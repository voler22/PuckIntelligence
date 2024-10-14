import datetime as dt
import math


def format_player_height_in_inches(height: str) -> int:
    """Convert height from feet and inches to inches.

    Parameters
    ----------
    height: str
        Height in feet and inches.

    Returns
    -------
    int
        Height in inches.

    Raises
    ------
    RuntimeError
        If height cannot be transformed.
    """
    if len(height) == 5:
        feet, inches = int(height[0]), int(height[2:4])
        return 12 * feet + inches
    elif len(height) == 4:
        feet, inches = int(height[0]), int(height[2])
        return 12 * feet + inches
    raise RuntimeError("Height cannot be transformed. Height: {}.format(height)")


def format_player_weight_in_lbs(weight: str) -> int:
    """Format weight.

    Parameters
    ----------
    weight: str
        Weight in pounds.

    Returns
    -------
    int
        Weight in pounds.
    """
    return int(weight.strip(" lb"))


def format_player_birthplace(birthplace: str) -> tuple:
    """Format birthplace.

    Parameters
    ----------
    birthplace: str
        Birthplace.

    Returns
    -------
    tuple
        Birth city, birth state, and birth country.
    """
    birthplace_ = birthplace.split(", ")
    try:
        # city, state, country
        return birthplace_[0], birthplace_[1], birthplace_[2]
    except IndexError:
        try:
            # city, country
            return birthplace_[0], None, birthplace_[1]
        except IndexError:
            # country
            return None, None, birthplace_[0]


def get_birthdate_and_age(date: str, run_date: dt.date) -> dt.date:
    """Convert date from string to datetime.

    Parameters
    ----------
    date: str
        Date in string format.
    run_date: dt.date
        Date for which script is running.

    Returns
    -------
    dt.date
        Date in datetime format.
    """
    try:
        date_ = date.split(" ")[0]
        date__ = dt.datetime.strptime(date_, "%m/%d/%Y").date()
    except ValueError:
        try:
            date__ = dt.datetime.strptime(date, "%b %d, %Y").date()
        except ValueError:
            raise ValueError("Date format unknown: {}".format(date))
    return date__, math.floor((run_date - date__).days / 365.25)
