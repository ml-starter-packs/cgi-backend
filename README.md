# cgi-backend-template
production-grade(ish) backend with `gevent` + `gunicorn` which makes use of Python's native `cgi` library to create a basic API.

In this example, accuracy is computed using `sklearn.metrics.accuracy_score` at the `/stats` endpoint as a dictionary, and the resulting table from `pandas.DataFrame.describe` is retured as a CSV at the `/info` endpoint.

# Instructions

Consult the `Makefile` to see what is being run with each of the following commands.

Run local server (this will also run `make install` to acquire dependencies):
```bash
make dev
```

Testing:
```bash
make test
```

Run containerized server:
```bash
make prod
```

# Minimal Example
For an API that does nothing but uses as little code as possible, read below:

Create `app.py` (shown below):

```python
import cgi
import io

def api(environ, start_response):
    # Route to requested handler
    if environ["PATH_INFO"] == "/api":
      return main(environ, start_response)
    start_response("404 Not Found", [])
    return [b"Page not found."]

def main(environ, start_response):
    form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
    byte_data = io.BytesIO(form["data"].value)
    str_data = io.TextIOWrapper(byte_data, encoding='utf-8').read()
    file_in_mem = io.StringIO(str_data)
    # do something with file, return response.
    out = "file received.\n"
    headers = [("Content-Type", "text/html")]
    start_response("200 OK", headers)
    return [out.encode("utf-8")]  # List[bytes]
```

To install the required dependencies, run
```bash
pip install gunicorn gevent
```


Run the API on port `5000` with:
```bash
gunicorn -b :5000 app:api --timeout 90 --worker-class gevent -w 1
```


Assuming `test.csv` exists (you can run `make test.csv` to create one), you can now test the API.

You can reach your endpoint with `curl` as follows:
```bash
curl -F data=@test.csv -H "Content-Type:multipart/form-data" -v http://localhost:5000/api
```

