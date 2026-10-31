# Lab 6 - Bike Share Rental coverage

I used the bike-share application from the assigned starter repository. The two starter tests passed, but they covered only 50% of its lines. The first pass below adds tests for invalid inputs, ride fees, every dock message, and the age checks for unlocking.

## Code coverage pass

From this folder, install the requirements and run:

```sh
python3 -m pip install -r requirements.txt
python3 -m coverage run --source=bike_share_rental -m pytest -q CodeCoverageTest_bike_share_rental_application.py
python3 -m coverage report -m
```

Result: **15 tests passed; 100% line coverage** (40 statements, 0 missed). See `code_coverage_result.png` for the command output.

The line-focused tests also cover 96% when branch measurement is turned on. The second pass adds cases for a normal ride and a longer subscriber ride to cover the remaining decisions.
