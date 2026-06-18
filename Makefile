load:
	python src/etl/loader.py

test:
	pytest tests/

clean:
	echo Cleaning project...

report:
	echo Generating report...

dashboard:
	echo Opening dashboard...

api:
	echo Starting API...

ratios:
	echo Calculating financial ratios...