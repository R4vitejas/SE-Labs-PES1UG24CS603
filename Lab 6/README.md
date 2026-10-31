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

## Branch coverage pass

Run both files together because the branch file adds to the first pass:

```sh
python3 -m coverage run --branch --source=bike_share_rental -m pytest -q CodeCoverageTest_bike_share_rental_application.py BranchCoverageTest_bike_share_rental_application.py
python3 -m coverage report -m
```

Result: **17 tests passed; 100% branch coverage** (40 statements, 30 branches, none missed or partial). See `branch_coverage_result.png` for the command output.

The extra tests matter because a line can run while one outcome of an `if` is still untested. The short free subscriber ride already visited the subscriber code, for example, but it returned before checking what a longer subscriber ride costs. The 60-minute cargo case checks that route. The ordinary standard ride checks the path without a peak or long-ride fee.

For comparison, the two starter tests had 50% line coverage and 44% total coverage with branch measurement. I left `bike_share_rental.py` unchanged from the assigned repository; the improvement comes from the tests.
