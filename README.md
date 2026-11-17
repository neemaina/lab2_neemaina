
# Lab 2: ALU Transcript Generator

A Python application that calculates a student's GPA and final status from a CSV of course grades, plus a Bash script that archives the CSV and logs the action.

## Files

| File | Purpose |
|---|---|
| `grade-evaluator.py` | Validates grades, calculates GPA, decides PASSED/FAILED, lists resubmission options |
| `organizer.sh` | Archives `grades.csv` with a timestamp, creates a fresh empty `grades.csv`, appends to `organizer.log` |
| `grades.csv` | Course grades (columns: `assignment,group,score,weight`) |

## How to run

```bash
python3 grade-evaluator.py
# Enter the name of the CSV file to process (e.g., grades.csv): grades.csv

chmod +x organizer.sh
./organizer.sh
```

Run `grade-evaluator.py` BEFORE `organizer.sh`. The organizer moves `grades.csv` into `archive/` and leaves a new empty `grades.csv` behind.

## CSV format

```
assignment,group,score,weight
Quiz,Formative,85,20
Midterm Project - Simple Calculator,Summative,70,20
```

- `group` is `Formative` or `Summative`
- `score` is 0-100
- `weight`: Formative weights total 60, Summative weights total 40

## Logic

- Each assignment contributes `score x weight / 100`.
- Total Grade = sum of contributions (out of 100).
- **GPA = (Total Grade / 100) x 5.0**
- Category % = category points / category weight x 100.
- **PASSED only if Formative >= 50% AND Summative >= 50%.** Otherwise FAILED.
- Resubmission: among formative assignments scoring below 50, the one(s) with the highest weight. If several share that weight, all are listed.

## Validation and edge cases

- File not found, empty file, missing header columns
- Empty rows and rows with missing fields are skipped and counted
- Non-numeric score or weight: row skipped with a warning
- Scores outside 0-100: error naming the assignment
- Total weight must be 100, Formative 60, Summative 40: each failure is reported
- Unknown group name: error
- No failed formative assignments: reports no resubmission needed

All errors print a clear message and exit without a traceback.

## organizer.sh behaviour

1. Creates `archive/` if missing
2. Moves `grades.csv` to `archive/grades_YYYYMMDD-HHMMSS.csv`
3. Creates a new empty `grades.csv`
4. Appends `[timestamp] Original: ... | Archived as: ...` to `organizer.log` (accumulates across runs)
5. Exits with an error message if `grades.csv` does not exist

## Sample output

```
Formative: 34.00/60 (56.67%)
Summative: 26.00/40 (65.00%)
Total Grade: 60.00/100
GPA: 3.0000

Final Status: PASSED

Eligible for resubmission (failed formative with the highest weight):
  - Group Exercise (score: 40, weight: 20)
  - Functions and Debugging Lab (score: 45, weight: 20)
```

No external libraries are used, only the standard `csv`, `sys` and `os` modules.
