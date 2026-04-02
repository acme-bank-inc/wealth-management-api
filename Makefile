.PHONY: install run clean

install:
	python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt

run:
	./venv/bin/python app.py

clean:
	rm -rf venv __pycache__ *.pyc
