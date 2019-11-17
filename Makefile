env:
	virtualenv env -p python3

deps:
	brew install cairo pkg-config freetype harfbuzz
install:
	env/bin/pip install -r requirements.txt

run:
	env/bin/python clockface.py

test:
	env/bin/python test.py
