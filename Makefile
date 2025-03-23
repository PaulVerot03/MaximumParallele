
tests:
	@python3 src/test.py

tests_pure:
	@python3 src/test.py -nogui

all: tests
