# cgi-backend-template
production-grade(ish) backend with `gevent` + `gunicorn` which makes use of Python's native `cgi` library to create a basic API.

In this example, accuracy is computed using `sklearn.metrics.accuracy_score`.

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

