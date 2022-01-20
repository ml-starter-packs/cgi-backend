dev: install
	./scripts/start.sh

install:
	pip install -r requirements.txt

build:
	docker build -t cgi-api .

prod: build
	docker run --rm -ti \
	  --name cgi-api-test \
	  -p 1337:1337 \
	  cgi-api

test-sh:
	@echo "Generating `test.csv`"
	echo "truth,pred" > test.csv
	@echo "Testing with shell script using `curl`"
	echo "0,1\n1,0\n1,1\n" >> test.csv
	./scripts/post.sh test.csv
	@echo " "

test-py:
	@echo "Testing with python script"
	./scripts/post.py
	@echo " "


test: test-sh test-py
