all: test

up:
	cd src/test && pytest test_e2e.py --snapshot-update -s

test:
	cd src/test && pytest test_e2e.py -v -s

clean:
	rm -rf src/test/parsing_results.json
	rm -rf src/test/snapshots
	python src/settings_data.py clean
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	rm -rf .pytest_cache