"""REST API for routes."""
import flask
import index
import pathlib
import re
from index.api.startup import stopwords
from index.api.startup import pageranks
from index.api.startup import inverted_index
import math

@index.app.route('/api/v1/', methods=["GET"])
def get_services():
    """Return API resource URLs."""
    context = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }

    return flask.jsonify(**context)


@index.app.route('/api/v1/hits/',  methods=["GET"])
def get_hits():
    """Return a list of hits."""
    # Get query and page rank weight
    query = flask.request.args.get("q", default='', type=str)
    weight = flask.request.args.get("w", default=0.5, type=float)

    context = {"hits": []}

    # Get list of documents that contain the query
    doc_ids = find_documents(query)
    ranks = []

    # Rank each documnt
    for doc_id in doc_ids:
        doc_and_rank = (calculate_score(query, doc_id, weight), doc_id)
        ranks.append(doc_and_rank)

    # Sort by the rank component of the pair
    ranks.sort(key=lambda x: x[0])

    # Add ranked documents to the context
    for doc_and_rank in ranks:
        context["hits"].append({
            "docid": doc_and_rank[1],
            "score": doc_and_rank[0]
        })

    # Return hits
    return flask.jsonify(**context)


def process_query(query):
    """Clean and process a query."""
    # Clean and put the words of the query into a list
    query_words = re.sub(r"[^a-zA-Z0-9 ]+", "", query).split()


def find_documents(query):
    """Find all documents containing all words of the query."""
    # Set of docs containing all words in the query
    # Initialize with documents that contain the first word of the query
    docs = inverted_index[query[0]]["docs"]
    doc_ids = { doc["doc_id"] for doc in docs }

    # Find doc ids of docs that contain all words in the query
    for word in query:
        # Skip the first word
        if word == query[0]:
            continue

        # Get all documents that contain the word
        word_docs = inverted_index[word]["docs"]

        # Set of doc ids that contain the word
        word_doc_ids = { doc["doc_id"] for doc in word_docs }

        # Intersect to get only docs that 
        doc_ids = doc_ids.intersection(word_doc_ids)

    return list(doc_ids)


def calculate_score(query, doc_id, weight):
    """Calculate the score of a document for a given query and weight."""
    pagerank = pageranks[doc_id]
    tf_idf = calcluate_tf_idf(query, doc_id)

    return weight * pagerank + (1 - weight)*tf_idf


def calcluate_tf_idf(query, doc_id):
    """Calculate the tf-idf for a document on a given query."""
    #TODO: fill in vectors
    query_vector = []
    doc_vector = []

    query_norm = calculate_sum_of_squres(query_vector)
    doc_norm = calculate_sum_of_squres(doc_vector)

    return (query_vector @ doc_vector) / (query_norm @ doc_norm)


def calculate_sum_of_squres(list):
    """Calculate the sum-of-squares of a list of values."""
    sum = 0
    for value in list:
        sum += math.pow(value, 2)
    return math.sqrt(sum)
