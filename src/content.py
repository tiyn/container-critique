from flask import url_for

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


def gen_arch_string():
    """
    Creates and returns a archive string of every file in ENTRY_DIR.

    Returns:
    string: html-formatted archive-string.
    """
    content_string = ""
    last_year = ""
    entries = db.get_entries()
    if entries is None:
        return ""
    entries.sort(key=lambda y: y[1])
    entries.reverse()
    entries.sort(key=lambda y: y[2])
    entries.reverse()
    for entry in entries:
        ident = entry[0]
        title = db.get_item_by_id(entry[1]).name
        year = entry[2]
        rating = entry[4]
        username = db.get_user_by_id(entry[5]).name
        if year != last_year:
            if last_year != "":
                content_string += "</ul>\n"
            content_string += "<h2>" + year + "</h2>\n"
            content_string += "<ul>\n"
            last_year = year
        content_string += "<li>"
        content_string += title + "<a href=\"" + \
            url_for("entry", ident=str(ident)) + "\"> " + \
            rating_to_star(rating) + " by " + username
        content_string += "</a><br></li>\n"

    return content_string


def gen_user_string(name):
    """
    Creates and returns a archive string of every file in ENTRY_DIR.

    Returns:
    string: html-formatted archive-string.
    """
    content_string = ""
    last_year = ""
    entries = db.get_entries_by_user(name)
    if entries is None:
        return ""
    entries.sort(key=lambda y: y[1])
    entries.reverse()
    entries.sort(key=lambda y: y[2])
    entries.reverse()
    for entry in entries:
        ident = entry[0]
        title = db.get_item_by_id(entry[1]).name
        year = entry[2]
        rating = entry[4]
        username = db.get_user_by_id(entry[5]).name
        if year != last_year:
            if last_year != "":
                content_string += "</ul>\n"
            content_string += "<h2>" + year + "</h2>\n"
            content_string += "<ul>\n"
            last_year = year
        content_string += "<li>"
        content_string += title + "<a href=\"" + \
            url_for("entry", ident=str(ident)) + "\"> " + \
            rating_to_star(rating)
        content_string += "</a><br></li>\n"

    return content_string


def gen_index_string():
    """
    Create and returns a string including every file in the database as an
    index.

    Returns:
    string: html-formatted index string.
    """
    content_string = ""
    entries = db.get_entries()
    if entries is None:
        return ""
    entries.reverse()
    for entry in entries:
        ident = entry[0]
        title = db.get_item_by_id(entry[1]).name
        year = entry[2]
        text = entry[3]
        rating = entry[4]
        username = db.get_user_by_id(entry[5]).name
        reviewed = entry[6]
        content_string += "<div class=\"entry\">\n"
        content_string += "<h1 id=\"" + str(ident) + "\"><a href=\"" + \
            url_for("entry", ident=str(ident)) + "\">" + title + \
            " (" + year + ") " + rating_to_star(rating) + "</a></h1>\n"
        content_string += "<small>rated " + str(rating) + \
            "/100 by <a href=\"" + url_for("user", name=username) + "\">" \
            + username + "</a> on " + str(reviewed) + "</small><br>"
        content_string += text
        content_string += "<br>"
        content_string += "</div>"
    return content_string


def gen_stand_string(ident):
    """
    Creates a html-string for an entry.

    Parameters:
    ident: ident of an entry.

    Returns:
    string: html-formatted string string equivalent to the file.
    """
    entry = db.get_entry_by_id(ident)
    content_string = ""
    if entry is not None:
        ident = entry.id
        title = db.get_item_by_id(entry.item_id).name
        year = entry.date
        text = entry.text
        rating = entry.rating
        username = db.get_user_by_id(entry.user_id).name
        reviewed = entry.reviewed
        content_string += "<h1>" + title + \
            " (" + year + ") "
        content_string += rating_to_star(rating)
        content_string += "</h1>\n"
        content_string += "<small>rated " + str(rating) + \
            "/100 by <a href=\"" + url_for("user", name=username) + "\">" + \
            username + "</a> on <a href=\"" + \
            url_for("index", _anchor=str(ident)) + "\">" + str(reviewed) + \
            "</a></small><br>\n"
        content_string += "<small>[<a href=\"" + \
            url_for("delete_entry", ident=ident) + \
            "\">delete entry</a>]</small>"
        content_string += text + "<br>\n"
    return content_string


def get_rss_string():
    """
    Create a rss-string of the blog and return it.

    Returns:
    string: rss-string of everything that is in the ENTRY_DIR.
    """
    content_string = ""
    entries = db.get_entries()
    if entries is None:
        return ""
    entries.reverse()
    for entry in entries:
        ident = entry[0]
        title = db.get_item_by_id(entry[1]).name
        year = entry[2]
        text = entry[3]
        rating = entry[4]
        username = db.get_user_by_id(entry[5]).name
        reviewed = entry[6]
        content_string += "<item>\n"
        content_string += "<title>" + title + "(" + year + ") " + \
            rating_to_star(rating) + " by " + username + "</title>\n"
        content_string += "<guid>" + \
            url_for("index", _anchor=str(ident), _external=True) + \
            "</guid>\n"
        content_string += "<pubDate>" + reviewed + "</pubDate>\n"
        content_string += "<description>" + text + "</description>\n"
        content_string += "</item>\n"
    return content_string
