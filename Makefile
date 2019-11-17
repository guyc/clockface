env:
	virtualenv env -p python3

deps:
	brew install cairo pkg-config freetype harfbuzz
install:
	env/bin/pip install -r requirements.txt

clockface.pdf:	clockface.py
	env/bin/python clockface.py

