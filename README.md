# cgi-backend-template
arguably production-grade backend with `gevent` + `gunicorn` which makes use of Python's native `cgi` library to create a basic API.

The primary purpose of this repository is educational, but it can readily be modified to turn python functions into an API if the requirements of the deployment are just "I need this to be accessible in the cloud."

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
For an API that does nothing except read CSV data and acknowledge the response of it, but uses as little code as possible, see below.
If you just need to expose some basic functionality behind a live endpoint, the example below can provide a sufficient template.
Once you have more than a single route to consider, the contents of this repository should serve as a template for that which is ready to scale with containerized deployment solutions.
If you need functionality such as argument-checking, customized header policies, authentication, etc, then it is suggested you reach for `flask` or `fastapi` instead of `cgi` to create your API.

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

## What about the `start_response` method in this example code?
Python has defined the Web Server Gateway Interface (WSGI) for any developer interested in implementing their own web server and it serves as a standard allowing users to use different web servers interchangeably. One key component to any request is to have a response regardless of the running process's status. In a more complex service, there can be multiple methods running to be able to generate a response. If in any stage there is a failure, we need to update the response header with the appropriate failure information. A buffer for a header is maintained by the web server and the user can add any information they like to it using the `start_response` method. This buffer is then used to generate the header that will be attached to the response received by the client. 

Interested readers can find more details [here](https://www.python.org/dev/peps/pep-3333/).  
