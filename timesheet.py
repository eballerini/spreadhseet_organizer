import re
from collections import defaultdict

import pyperclip


def parse_time(t):
    """Convert time in format H or H.MM to float hours."""
    parts = t.split('.')
    hours = int(parts[0])
    minutes = int(parts[1]) if len(parts) > 1 else 0
    return hours + (minutes / 60) * 100 / 100


def adjust_for_pm(start, end):
    """Adjust end time if it's numerically less than start time (PM adjustment)."""
    if end < start:
        end += 12
    return end


def calculate_duration(start_str, end_str):
    """Return duration from start to end time in hours with 0-100 minute conversion."""
    start = parse_time(start_str)
    end = parse_time(end_str)
    end = adjust_for_pm(start, end)
    return round(end - start, 2)


def main():
    print("Enter task log (Ctrl+D or Ctrl+Z to finish):")
    input_lines = []
    try:
        while True:
            line = input()
            input_lines.append(line)
    except EOFError:
        pass

    task_times = defaultdict(float)
    total_hours = 0.0

    for line in input_lines:
        line = line.strip()
        if not re.match(r'^\d', line):  # Ignore lines that don't start with a digit
            continue

        match = re.match(r'^(\d{1,2}(?:\.\d{1,2})?)-(\d{1,2}(?:\.\d{1,2})?)\s+(.*)', line)
        if not match:
            continue

        start_time, end_time, task = match.groups()
        if task.lower().startswith("break"):
            continue

        duration = calculate_duration(start_time, end_time)
        task_times[task] += duration
        total_hours += duration

    output_lines = [f"{task} ({round(time, 2)})" for task, time in task_times.items()]

    # Display output
    for line in output_lines:
        print(line)

    print(f"\nTotal hours: {round(total_hours, 2)}")

    # Copy to clipboard with newlines (for single cell in Google Sheets)
    clipboard_content = "\n".join(output_lines)
    pyperclip.copy(clipboard_content)
    print("\n✅ Output copied to clipboard with line breaks!")


if __name__ == "__main__":
    main()
