#!/usr/bin/env python


import csv
import io
import json
import requests


def post_data(
    data, host="http://localhost:1337", dest="/api", sorted=False, strip=False
) -> str:
    """
    Creates CSV file in memory and posts it to `url` as multipart/form-data.
    """
    url = host + dest
    data = dict_to_csv_str(data, sorted=sorted)
    r = requests.post(url, files={"data": data})
    if strip:
        return strip_html(r)
    return r.content.decode("utf-8")


def dict_to_csv_str(data: dict, sorted: bool = False) -> str:
    """
    Converts dictionary to in-memory CSV

    Parameters
    ----------
    data: dict
        Dictionary of data
    sorted: bool = False
        Should the keys in the data dictionary be sorted?

    Returns
    -------
    str
        CSV-file ready for sending with `requests.post`

    """
    if sorted:
        keys = sorted(data.keys())
    else:
        keys = list(data.keys())

    inmem = io.StringIO()
    csv_writer = csv.writer(inmem)
    csv_writer.writerow(keys)
    csv_writer.writerows(zip(*[data[k] for k in keys]))
    return inmem.getvalue()


def strip_html(response):
    """
    Strips HTML header/footer from a response.
    This is useful when trying to embed HTML into
    an existing page through use of an external API.
    """
    return (
        response.content.decode("utf-8")
        .replace("<!DOCTYPE html>\n\n<html>", "")
        .replace("</html>", "")
        .replace("<html>", "")
    )


if __name__ == "__main__":

    data = {"truth": [0, 1, 2], "pred": [1, 1, 0]}

    response = post_data(data, dest="/info")
    print("INFO:")
    print(response)
    response = post_data(data, dest="/stats")
    print("STATS:")
    print(response)
