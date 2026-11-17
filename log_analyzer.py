# Error Log Analyzer
# Uses: class (OOP), file handling (open/read/write), exception handling
# Log line format: 2026-11-10 09:02:45 ERROR [database] Connection timeout


class LogAnalyzer:
    def __init__(self):
        self.warnings = 0
        self.errors = 0
        self.malformed = 0
        self.sources = {}          # source -> count of errors + warnings
        self.error_msgs = {}       # message -> count
        self.warning_msgs = {}     # message -> count
        self.file_errors = []      # file related problems

    def read_file(self, filename):
        try:
            with open(filename, "r") as f:
                for line in f:
                    self.check_line(line.strip())
            return True
        except FileNotFoundError:
            self.file_errors.append(filename + " -> File not found")
        except PermissionError:
            self.file_errors.append(filename + " -> Permission denied")
        except Exception as e:
            self.file_errors.append(filename + " -> " + str(e))
        return False

    def check_line(self, line):
        if line == "":
            return
        parts = line.split(" ", 4)          # date, time, level, [source], message
        if len(parts) < 5 or not parts[3].startswith("["):
            self.malformed += 1
            return

        level = parts[2]
        source = parts[3].strip("[]")
        message = parts[4]

        if level == "ERROR":
            self.errors += 1
            self.add(self.error_msgs, message)
        elif level == "WARNING":
            self.warnings += 1
            self.add(self.warning_msgs, message)
        else:
            return                          # INFO lines are ignored

        self.add(self.sources, source)
        if "file" in message.lower() or "permission" in message.lower() or "disk" in message.lower():
            self.file_errors.append(level + " [" + source + "] " + message)

    def add(self, dictionary, key):
        dictionary[key] = dictionary.get(key, 0) + 1

    def top5(self, dictionary):
        items = list(dictionary.items())
        items.sort(key=lambda x: x[1], reverse=True)
        return items[:5]

    def report(self):
        text = "\n" + "*" * 50 + "\n"
        text += "*" + "E R R O R   L O G   A N A L Y Z E R".center(48) + "*\n"
        text += "*" * 50 + "\n\n"

        text += "1. Total Warnings : " + str(self.warnings) + "\n"
        text += "2. Total Errors   : " + str(self.errors) + "\n"
        text += "   Malformed lines: " + str(self.malformed) + "\n\n"

        text += "3. Errors/Warnings by Source:\n"
        for source, count in self.top5(self.sources):
            text += "   " + source.ljust(12) + ": " + str(count) + "\n"

        text += "\n4. File Errors:\n"
        if not self.file_errors:
            text += "   None\n"
        for item in self.file_errors:
            text += "   - " + item + "\n"

        text += "\n5. Top 5 Errors:\n"
        for msg, count in self.top5(self.error_msgs):
            text += "   " + str(count) + "x  " + msg + "\n"

        text += "\n   Top 5 Warnings:\n"
        for msg, count in self.top5(self.warning_msgs):
            text += "   " + str(count) + "x  " + msg + "\n"
        return text

    def save_report(self, text, filename="report.txt"):
        try:
            with open(filename, "w") as f:
                f.write(text)
            print("Report saved to", filename)
        except Exception as e:
            print("Could not save report:", e)


# ---------------- main program ----------------
filename = input("Enter log file name (press Enter for app.log): ").strip()
if filename == "":
    filename = "app.log"

analyzer = LogAnalyzer()
if analyzer.read_file(filename):
    result = analyzer.report()
    print(result)
    analyzer.save_report(result)
else:
    print("Error:", analyzer.file_errors[0])
