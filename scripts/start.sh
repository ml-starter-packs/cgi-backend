#!/bin/sh
gunicorn -b :1337 main:app --timeout 90 --worker-class gevent -w 1
