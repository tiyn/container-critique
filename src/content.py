from database import Database

db = Database()


def rating_to_star(rating):
    """
    Creates a string with stars based on the rating.

    Parameters:
    rating: rating with minimum of 0 and maximum of 100.

    Returns:
    string: unicode-formatted star-rating string.
    """
    res = u"\u272D"*int(rating/20)
    if rating/20 % 1 >= 0.5:
        res += u"\u00BD"
    return res
