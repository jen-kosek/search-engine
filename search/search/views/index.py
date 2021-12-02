"""
ask485 index (main) view.

URLs include:
/
"""

import flask
import search
import requests
from threading import Thread
import time
import heapq


@search.app.route('/', methods=["GET"])
def show_index():
    context = {"docs": [], 
               "query": '', 
               "weight": "0.5", 
               "show_results": False}

    # First load
    if "q" not in flask.request.args:
        return flask.render_template("index.html", **context)

    # Get query and weight
    query = flask.request.args.get("q", default='', type=str)
    weight = flask.request.args.get("w", default=0.5, type=float)

    # Update context
    context["show_results"] = True
    context["query"] = query
    context["weight"] = str(weight).rstrip('0').rstrip('.')

    # Get query results if non empty query
    if query != '':
        # Get top 10 hits
        docs = get_hits(query, weight)

        # Get info for eahc hit
        context["docs"] = get_info(docs)

    return flask.render_template("index.html", **context)


def request_hits(url, query, weight, hits):
    """Request hits from a given index server."""
    # Make request and get response
    payload = {'q': query, 'w': weight}
    response = requests.get(url, params=payload)
    response_dict = response.json()

    # Add hits to list 
    for hit in response_dict["hits"]:
        hits.append(hit)


def get_hits(query, weight):
    """Get hits from index servers and return top 10 hits."""
    # List to store hits
    hits = []
    for index, _ in enumerate(search.app.config["SEARCH_INDEX_SEGMENT_API_URLS"]):
        hits.append([])

    # Make a thread for each server request
    threads = []
    for index, server in enumerate(search.app.config["SEARCH_INDEX_SEGMENT_API_URLS"]):
        threads.append(Thread(target=request_hits,
                       args=(server, query, weight, hits[index], )))

    # Start each thread
    for thread in threads:
        thread.start()

    # Wait to get responses from each server
    num_alive = len(search.app.config["SEARCH_INDEX_SEGMENT_API_URLS"])
    while num_alive != 0:
        num_alive = 0
        for thread in threads:
            if thread.is_alive():
                num_alive += 1
        time.sleep(1)

    # Sort by score and return top 10 docids
    merged_hits = heapq.merge(*hits, key=lambda x: (x["score"], -x["docid"]), reverse=True)
    top_10 = [hit for hit in merged_hits][:10]
    return [hit["docid"] for hit in top_10]


def get_info(docs):
    """Query the db and return info on the given docs."""
    info = []
    
    # Connect to database
    connection = search.model.get_db()

    # Query database for users that logname is following
    for doc in docs:
        cur = connection.execute(
            "SELECT * "
            "FROM Documents "
            "WHERE docid=?",
            [doc]
        )
        info.append(cur.fetchone())

    return info