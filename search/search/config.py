import pathlib

SEARCH_INDEX_SEGMENT_API_URLS = [
    "http://localhost:9000/api/v1/hits/",
    "http://localhost:9001/api/v1/hits/",
    "http://localhost:9002/api/v1/hits/",
]

ASK485_ROOT = pathlib.Path(__file__).resolve().parent

DATABASE_FILENAME = ASK485_ROOT/'var'/'index.sqlite3'