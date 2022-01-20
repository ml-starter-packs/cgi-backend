#!/usr/bin/env python

import cgi
import io
from typing import List, Dict

import pandas as pd
import sklearn.metrics as mt


def app(environ, start_response):
    # Route to requested handler.
    if environ["PATH_INFO"] == "/stats":
        return main(environ, start_response)
    if environ["PATH_INFO"] == "/info":
        return info(environ, start_response)
    start_response("404 Not Found", [])
    return [b"Page not found."]


def get_data(environ) -> io.StringIO:
    form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
    data = io.BytesIO(form["data"].value)
    data = io.TextIOWrapper(data, encoding="utf-8").read()
    data = io.StringIO(data)  # file-like object
    return data


def return_data(data: str, start_response) -> List[str]:
    headers = [("Content-Type", "text/html")]
    start_response("200 OK", headers)
    return [data.encode("utf-8")]


def compute_stats(data: io.StringIO) -> str:
    df = pd.read_csv(data)
    score = mt.accuracy_score(y_true=df["truth"], y_pred=df["pred"])
    out = str({"accuracy": score})
    return out


def summary_csv(data: io.StringIO) -> str:
    df = pd.read_csv(data)
    out = df.describe().to_csv(index=True)
    return out


def main(environ, start_response):
    data = get_data(environ)
    out = compute_stats(data)
    return return_data(out, start_response)


def info(environ, start_response):
    data = get_data(environ)
    out = summary_csv(data)
    return return_data(out, start_response)