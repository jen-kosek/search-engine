"""
ask485 index (main) view.

URLs include:
/
"""

import flask
import index
from requests import HTTPSession
from threading import Thread
import config
import time


@index.app.route('/')
def show_index():
    # Get query and weight
    query = flask.request.args("q", default='', type=str)
    weight = flask.request.args("w", default=0.5, type=float)

    context = {"hits": []}

    # Get query results if non empty query
    if query != '':
        # Get top 10 hits
        docs = get_hits(query, weight)

        # Get info for eahc hit
        context["hits"] = get_info(docs)

    return flask.render_template("index.html", **context)


def request_hits(url, query, weight, hits):
    """Request hits from a given index server."""
    # Make a connection pool.
    http = HTTPSession()

    # Make request and get response
    payload = {'q': query, 'w': weight}
    response = http.request('get', url, params=payload)
    response_dict = response.json().loads()

    # Add hits to list 
    for hit in response_dict["hits"]:
        response.append(hit)


def get_hits(query, weight):
    """Get hits from index servers and return top 10 hits."""
    # List to store hits
    hits = []

    # Make a thread for each server request
    threads = []
    for server in config.SEARCH_INDEX_SEGMENT_API_URLS:
        threads.append(Thread(target=request_hits, args=(server, query, weight, hits, )))

    # Start each thread
    for thread in threads:
        thread.start()

    # Wait to get responses from each server
    num_alive = len(config.SEARCH_INDEX_SEGMENT_API_URLS)
    while num_alive != 0:
        num_alive = 0
        for thread in threads:
            if thread.is_alive():
                num_alive += 1
        time.sleep(1)

    # Sort by score and return top 10 docids
    hits.sort(key=lambda x: (x["score"], -x["docid"]), reverse=True)
    return [hit["docid"] for hit in hits[:10]]


def get_info(docs):
    """Query the db and return info on the given docs."""
    info = []
    
    # Connect to database
    connection = index.model.get_db()

    # Query database for users that logname is following
    for doc in docs:
        cur = connection.execute(
            "SELECT * "
            "WHERE docid=?",
            [doc]
        )
        info.append(cur.fetchone())

    return info