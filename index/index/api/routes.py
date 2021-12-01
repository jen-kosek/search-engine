"""REST API for routes."""
import re
import pathlib
import math
import flask
import index


# GLOBALS
stopwords = []       # list of stopwords
pageranks = {}       # dictionary of doc_id, pagerank pairs
inverted_index = {}  # dictionary of words and inverted index info


@index.app.before_first_request
def startup():
    """Load inverted index, pagerank, and stopwords into memory."""
    index_dir = pathlib.Path(__file__).parent.parent
    read_stopwords(index_dir)
    read_pagerank(index_dir)
    read_inverted_index(index_dir)


def read_stopwords(index_dir):
    """Read stopwords into list."""
    filepath = index_dir / "stopwords.txt"
    with filepath.open() as file:
        for line in file:
            stopwords.append(line.strip())


def read_pagerank(index_dir):
    """Read pagerank into dictionary."""
    filepath = index_dir / "pagerank.out"
    with filepath.open() as file:
        for line in file:
            doc_id, rank = line.strip().split(',')
            pageranks[int(doc_id)] = float(rank)


def read_inverted_index(index_dir):
    """Read inverted index into dictionary."""
    filepath = index_dir / "inverted_index" / index.app.config['INDEX_PATH']
    with filepath.open() as file:
        for line in file:
            # Divide the line in to a list
            parts = line.split()

            # Store the idf and document info
            inverted_index[parts[0]] = {
                "idf": float(parts[1]),
                "docs": []
            }

            # Get all the documents the term appears in
            i = 2
            while i < len(parts):
                inverted_index[parts[0]]["docs"].append({
                    "docid": int(parts[i]),
                    "tf": float(parts[i+1]),
                    "nf": float(parts[i+2])
                })

                i += 3


@index.app.route('/api/v1/', methods=["GET"])
def get_services():
    """Return API resource URLs."""
    context = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }

    return flask.jsonify(**context)


@index.app.route('/api/v1/hits/', methods=["GET"])
def get_hits():
    """Return a list of hits."""
    # Get query and page rank weight
    query = flask.request.args.get("q", default="", type=str)
    weight = flask.request.args.get("w", default=0.5, type=float)

    context = {"hits": []}

    # Turn query into parsed list
    clean_query = process_query(query)

    # Get list of documents that contain the query
    doc_ids = find_documents(clean_query)
    ranks = []

    # Rank each documnt
    for doc_id in doc_ids:
        doc_and_rank = (calculate_score(clean_query, doc_id, weight), doc_id)
        ranks.append(doc_and_rank)

    # Sort high to low score, then low to high id
    ranks.sort(key=lambda x: (x[0], -x[1]), reverse=True)

    # Add ranked documents to the context
    for doc_and_rank in ranks:
        context["hits"].append({
            "docid": doc_and_rank[1],
            "score": doc_and_rank[0]
        })

    # Return hits
    return flask.jsonify(**context)


def process_query(query):
    """Clean and process a query, returning a list of words."""
    # Clean and lowercase the string
    lower_words = re.sub(r"[^a-zA-Z0-9 ]+", "", query).casefold()

    # Copy over non-stop words into output list
    output_list = []
    for word in lower_words.split():
        # Skip stopwords
        if word in stopwords:
            continue
        output_list.append(word)

    # Return the output list
    return output_list


def find_documents(query):
    """Find all documents containing all words of the query."""
    # Check that the first word in the query appears in a doc
    if query[0] not in inverted_index:
        return []

    # Set of docs containing all words in the query
    # Initialize with documents that contain the first word of the query
    docs = inverted_index[query[0]]["docs"]
    doc_ids = {doc["docid"] for doc in docs}

    # Find doc ids of docs that contain all words in the query
    for word in query:
        # Skip the first word
        if word == query[0]:
            continue

        # Get all documents that contain the word
        if word not in inverted_index:
            return []
        word_docs = inverted_index[word]["docs"]

        # Set of doc ids that contain the word
        word_doc_ids = {doc["docid"] for doc in word_docs}

        # Intersect to get only docs that contain all query words
        doc_ids = doc_ids & word_doc_ids

    return list(doc_ids)


def calculate_score(query, doc_id, weight):
    """Calculate the score of a document for a given query and weight."""
    pagerank = pageranks[doc_id]
    tf_idf = calculate_tf_idf(query, doc_id)

    return weight * pagerank + (1 - weight) * tf_idf


def calculate_tf_idf(query, doc_id):
    """Calculate the tf-idf for a document on a given query."""
    # Make blank vectors for query and doc
    query_vector = []
    doc_vector = []

    # Get frequency of each term in query
    query_frequency = {}
    for term in query:
        if term not in query_frequency:
            query_frequency[term] = 1
        else:
            query_frequency[term] += 1

    # Calculate each position in query and doc vectors
    doc_norm = -1
    for term, query_freq in query_frequency.items():
        # Add query vector term
        query_vector.append(
            inverted_index[term]["idf"] * query_freq)

        # Find document tf and nf
        for doc in inverted_index[term]["docs"]:
            if doc["docid"] == doc_id:
                # Add document vector term
                doc_vector.append(inverted_index[term]["idf"] * doc["tf"])

                # Find doc nf during first loop
                if doc_norm == -1:
                    doc_norm = math.sqrt(doc["nf"])

                break

    # Calcualte nf for query
    query_norm = math.sqrt(sum([math.pow(value, 2)
                           for value in query_vector]))

    # Calculate dot product of query and doc vectors
    vector_dot_product = sum([query_vector[i]*doc_vector[i]
                             for i in range(len(query_vector))])

    return vector_dot_product / (query_norm * doc_norm)
