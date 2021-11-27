"""Startup."""
import flask
import index
import pathlib

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
    with open(f"{index_dir}/stopwords.txt") as file:
        stopwords = [line.strip() for line in file.readlines()]


def read_pagerank(index_dir):
    """Read pagerank into dictionary."""
    with open(f"{index_dir}/pagerank.out") as file:
        for line in file.readlines():
            doc_id, rank = line.split(',')
            pageranks[doc_id] = rank


def read_inverted_index(index_dir):
    """Read inverted index into dictionary."""
    with open(f"{index_dir}/pagerank.out") as file:
        for line in file.readlines():
            # Divide the line in to a list
            parts = line.split()
            
            # Store the idf and document info
            inverted_index[parts[0]] = {
                "idf": parts[1],
                "docs": []
            }

            # Get all the documents the term appears in 
            i = 2
            while i < parts.size:
                inverted_index[parts[0]]["docs"].append({
                    "doc_id": parts[i],
                    "tf": parts[i+1],
                    "nf": parts[i+2]
                })

                i += 3