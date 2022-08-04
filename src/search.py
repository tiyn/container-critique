import os
import re

from whoosh import scoring
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser

import config
from database import Database

CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')


def remove_html_tags(text):
    """
    Convert a text from html formatted to unformatted.

    Parameters:
    text (str): text to clean

    Returns:
    str: text without html tags
    """
    res = re.sub(CLEANR, '', text)
    return res


def create_search_index():
    """
    Create the index data to search all entries.
    """
    db = Database()
    schema = Schema(title=TEXT(stored=True),
                    path=ID(stored=True), content=TEXT(stored=True))
    if not os.path.exists(config.INDEX_DIR):
        os.mkdir(config.INDEX_DIR)
    ix = create_in(config.INDEX_DIR, schema)
    writer = ix.writer()
    for entry in db.get_entries():
        path = str(entry.id)
        text = entry.item.name + " " + entry.item.date + " " + entry.text + \
            " by " + entry.user.name + " " + entry.date
        writer.add_document(title=entry.item.name, path=path, content=text)
    writer.commit()


def ft_search_times(query_str, number):
    """
    Search for a given term and returns a specific amount of results.

    Parameters:
    query_str (str): term to search for
    number (int): number of results to return

    Returns:
    List(Entry): list of entries that matched the search
    """
    ix = open_dir(config.INDEX_DIR)
    results = []
    db = Database()
    with ix.searcher(weighting=scoring.BM25F) as s:
        query = QueryParser("content", ix.schema).parse(query_str)
        matches = s.search(query, limit=number)
        for match in matches:
            results.append(db.get_entry_by_id(match["path"]))
    return results


def ft_search(query_str):
    """
    Search for a given term and show the predefined amount of results.

    Parameters:
    query_str (str): term to search for

    Returns:
    List(Entry): list of entries that matched the search
    """
    return ft_search_times(query_str, config.SEARCH_NUMBER)
