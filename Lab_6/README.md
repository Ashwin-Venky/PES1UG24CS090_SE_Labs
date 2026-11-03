# Lab 6: Code and Branch Coverage

Name - Ashwin Venkatesh

SRN - PES1UG24CS090

## Application

The weather alert classifier assigns `none`, `advisory`, `watch`, or `warning`
based on wind speed, rainfall, soil saturation, temperature, and humidity.
`overall_alert()` returns the highest severity in a list and rejects unknown
alert names with `ValueError`.

Source: <https://github.com/SETAPESU26/L6_L7_32_weather_alert/tree/main/lab6>.
Downloaded using the repository ZIP and extracted into `Lab_6`.
The supplied application and starter tests are unchanged.

## Setup

Run from `Lab_6`:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Tested with Python 3.13.0, pytest 9.2.0, and coverage.py 7.17.0.
The configuration measures only `weather_alert.py`, so executing the test
files does not inflate the application coverage.

## Initial coverage

The two starter tests pass. They execute 12 of the application's 38 executable
statements (31.58%) and 4 of its 28 branch destinations (14.29%). In branch mode,
coverage.py's combined statement-and-branch percentage is 24.24%.

The original run output and JSON measurements are in
`reports/initial_line.*` and `reports/initial_branch.*`.

## Code coverage

`CodeCoverageTest_weather_alert.py` contains 16 cases covering all return
statements and the invalid-alert exception. Heat tests use humidity 60, which
adds 2 to the temperature index.

```sh
python -m coverage run -m pytest -q CodeCoverageTest_weather_alert.py
python -m coverage report -m
```

Result: **16 passed; 38/38 statements covered; 100% line coverage**.
See `screenshots/code_coverage.png` and `reports/line.txt`.

Line coverage checks whether a statement executes. It does not show whether
both outcomes of every decision execute. Branch coverage is measured separately.

## Branch coverage

`BranchCoverageTest_weather_alert.py` contains 66 cases covering all decisions
and the values immediately below, at, and above each alert threshold:

- Wind speed thresholds of 39, 62, and 89 km/h.
- Rainfall thresholds of 10 and 50 mm/hour with both soil saturation values.
- Heat index thresholds of 35, 40, and 45 with humidity below, at, and above 40.
- Empty, increasing, decreasing, repeated, and mixed alert lists.
- Invalid alerts, including an invalid entry after a warning.

```sh
python -m coverage run --branch -m pytest -q BranchCoverageTest_weather_alert.py
python -m coverage report -m
python -m coverage json -o reports/branch.json
```

Result: **66 passed; 38/38 statements and 28/28 branch destinations covered**.
Line coverage and branch coverage are both **100%**, with no missing lines or
partial branches. See `screenshots/branch_coverage.png` and `reports/branch.txt`.
In branch mode, the report's `Cover` column combines statement and branch
coverage; the JSON report separately confirms 100% for each metric.

## Results

| Suite | Cases passed | Line coverage | Branch coverage |
| --- | ---: | ---: | ---: |
| Starter tests | 2 | 31.58% | 14.29% |
| Code coverage tests | 16 | 100% | Measured separately |
| Branch coverage tests | 66 | 100% | 100% |

The screenshots are captures of the actual macOS Terminal runs. Only final
results above the required 90% threshold are included as screenshots.

## Run all tests

```sh
python -m coverage run --branch -m pytest -q
python -m coverage report -m
```

`pytest.ini` includes the two handout-style test filenames in test discovery.
All 84 cases pass together, including the two original starter cases.
The line and branch test suites and their screenshots are saved in separate
commits. The ZIP archive, virtual environment, and raw coverage databases are
kept out of version control.

100% coverage means every measured statement and branch destination executed.
It does not prove correctness for every possible input or full path coverage.
