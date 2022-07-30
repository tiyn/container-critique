import config
from database import Database

db = Database()


def gen_arch_string():
    """
    Creates and returns a archive string of every file in ENTRY_DIR.

    Returns:
    string: html-formatted archive-string
    """
    content_string = ""
    last_year = ""
    entries = db.get_entries()
    if entries is None:
        return ""
    entries.sort(key=lambda y: y[2])
    for entry in entries:
        ident = entry[0]
        title = entry[1]
        year = entry[2]
        rating = entry[4]
        if year != last_year:
            if last_year != "":
                content_string += "</ul>\n"
            content_string += "<h2>" + year + "</h2>\n"
            content_string += "<ul>\n"
            last_year = year
        content_string += "<li>"
        content_string += "[<a href=\"" + "/index.html#" + str(ident) + \
            "\">link</a> - <a href=\"/entry/" + \
            str(ident) + "\">standalone</a>] "
        content_string += title + " - " + str(rating) + "/100<br>"
        content_string += "</li>\n"

    return content_string


def gen_index_string():
    """
    Create and returns a string including every file in the database as an index.

    Returns:
    string: html-formatted index string
    """
    content_string = ""
    entries = db.get_entries()
    if entries is None:
        return ""
    entries.reverse()
    for entry in entries:
        ident = entry[0]
        title = entry[1]
        year = entry[2]
        text = entry[3]
        rating = entry[4]
        username = db.get_user_by_id(entry[5])[1]
        reviewed = entry[6]
        content_string += "<div class=\"entry\">\n"
        content_string += "<h1 id=\"" + \
            str(ident) + "\">" + title + " (" + year + ") - " + \
            str(rating) + "/100</h1>\n"
        content_string += "[<a href=\"" + "/entry/" + \
            str(ident) + "\">" + "standalone" + "</a>]<br>\n"
        content_string += text
        content_string += "<br>"
        content_string += "<small>" + \
            str(reviewed) + " by " + username + "</small>"
        content_string += "</div>"
    return content_string


def gen_stand_string(ident):
    """
    Creates a html-string for an entry.

    Parameters:
    ident: ident of an entry.

    Returns:
    string: html-formatted string string equivalent to the file
    """
    entry = db.get_entry_by_id(ident)
    content_string = ""
    if entry is not None:
        ident = entry[0]
        title = entry[1]
        year = entry[2]
        text = entry[3]
        rating = entry[4]
        username = db.get_user_by_id(entry[5])[1]
        reviewed = entry[6]
        content_string += "<h1>" + title + \
            " (" + year + ") - " + str(rating) + "/100 </h1>\n"
        content_string += "["
        content_string += "<a href=\"" + "/index.html#" + \
            str(ident) + "\">" + "link" + "</a>"
        content_string += "]<br>\n"
        content_string += "<small>" + \
            str(reviewed) + " by " + username + "</small>"
        content_string += "<br>\n"
        content_string += text
        content_string += "<br>"
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
        title = entry[1]
        year = entry[2]
        text = entry[3]
        rating = entry[4]
        username = db.get_user_by_id(entry[5])[1]
        reviewed = entry[6]
        content_string += "<item>\n"
        content_string += "<title>" + title + \
            "(" + year + ") " + str(rating) + "/100 </title>\n"
        content_string += "<guid>" + config.WEBSITE + \
            "/index.html#" + str(ident) + "</guid>\n"
        content_string += "<pubDate>" + reviewed + "</pubDate>\n"
        content_string += "<description>"
        content_string += text
        content_string += "</description>\n"
        content_string += "</item>\n"
    return content_string
