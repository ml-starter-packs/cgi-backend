#!/usr/bin/env python

import cgi
import io
from typing import List

import pandas as pd  # type: ignore
import sklearn.metrics as mt  # type: ignore


def app(environ, start_response) -> List[bytes]:
    # Route to requested handler.
    if environ["PATH_INFO"] == "/stats":
        return main(environ, start_response, compute_stats)
    if environ["PATH_INFO"] == "/info":
        return main(environ, start_response, summary_csv)
    start_response("404 Not Found", [])
    return [b"Page not found."]


def get_data(environ) -> io.StringIO:
    form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
    byte_data = io.BytesIO(form["data"].value)
    data: str = io.TextIOWrapper(byte_data, encoding="utf-8").read()
    return io.StringIO(data)  # file-like object


def return_data(data: str, start_response) -> List[bytes]:
    headers = [("Content-Type", "text/html")]
    start_response("200 OK", headers)
    return [data.encode("utf-8")]


def compute_stats(data: io.StringIO) -> str:
    df = pd.read_csv(data)
    accuracy_score = mt.accuracy_score(y_true=df["truth"], y_pred=df["pred"])
    return str({"accuracy": accuracy_score})


def summary_csv(data: io.StringIO) -> str:
    return pd.read_csv(data).describe().to_csv(index=True)


def main(environ, start_response, function=compute_stats) -> List[bytes]:
    out = function(get_data(environ))
    return return_data(out, start_response)
