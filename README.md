# Error Log Analyzer

A command-line Python tool that reads an application log file and produces a summary report of errors and warnings: how many there are, which components produce them, which messages repeat most, and which ones point to file or disk problems.

I built this to practise object-oriented programming, file handling and exception handling in Python.

## Features

- Counts total **errors** and **warnings** (INFO lines are skipped)
- Detects and counts **malformed lines** instead of crashing on them
- Ranks the **sources** (components) with the most errors and warnings
- Flags **file, permission and disk** related issues
- Lists the **top 5 most frequent** error and warning messages
- Prints the report and **saves it to `report.txt`**
- Handles a missing file or a file it can't read without crashing

## Log format

Each line is expected to look like this:

```
YYYY-MM-DD HH:MM:SS LEVEL [source] message
```

Example:

```
2026-11-10 09:02:45 ERROR [database] Connection timeout
```

Supported levels: `ERROR`, `WARNING`, `INFO`.

## How to run

Requires Python 3 (no external libraries).

```bash
git clone https://github.com/anirudhr-05/error-log-analyzer.git
cd error-log-analyzer
python log_analyzer.py
```

When asked, type the log file name, or press Enter to use the included `app.log`.

## Sample output

```
**************************************************
*      E R R O R   L O G   A N A L Y Z E R       *
**************************************************

1. Total Warnings : 3
2. Total Errors   : 5
   Malformed lines: 1

3. Errors/Warnings by Source:
   database    : 3
   storage     : 2
   api         : 2
   auth        : 1

4. File Errors:
   - ERROR [storage] Disk full on /var/data
   - ERROR [storage] Permission denied writing report

5. Top 5 Errors:
   2x  Connection timeout
   1x  Disk full on /var/data
   1x  Permission denied writing report
   1x  Query failed

   Top 5 Warnings:
   2x  Slow response time
   1x  Password attempt limit near

Report saved to report.txt
```

## Project structure

```
error-log-analyzer/
├── log_analyzer.py   # main program (LogAnalyzer class)
├── app.log           # sample log file to try it with
└── README.md
```

## How it works

- `read_file()` opens the log and catches `FileNotFoundError`, `PermissionError` and other errors.
- `check_line()` splits each line into date, time, level, source and message, and updates the counters.
- `top5()` sorts the counts and returns the five most frequent items.
- `report()` builds the text report and `save_report()` writes it to a file.

## Planned improvements

- Support more levels such as `WARN` and `CRITICAL`
- Filter by date or time range
- Command-line arguments with `argparse`
- Export the report as CSV or JSON
- Unit tests with `pytest`

## What I learned

- Structuring a program around a class
- Reading and writing files safely with `with open(...)`
- Handling specific exceptions instead of letting the program crash
- Counting and sorting data with dictionaries
