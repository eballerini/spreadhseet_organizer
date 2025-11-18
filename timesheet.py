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
    """If end time is numerically less than start, assume PM."""
    if end < start:
        end += 12
    return end


def calculate_duration(start_str, end_str):
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
    task_order = []  # Preserve order of tasks
    total_hours = 0.0

    for line in input_lines:
        line = line.strip()
        if not re.match(r'^\d', line):
            continue

        match = re.match(r'^(\d{1,2}(?:\.\d{1,2})?)-(\d{1,2}(?:\.\d{1,2})?)\s+(.*)', line)
        if not match:
            continue

        start_time, end_time, task = match.groups()
        if task.lower().startswith("break"):
            continue

        if task not in task_order:
            task_order.append(task)

        duration = calculate_duration(start_time, end_time)
        task_times[task] += duration
        total_hours += duration

    # Prepare output lines
    output_lines = [f"{task} ({round(time, 2)})" for task, time in task_times.items()]

    # Print results
    for line in output_lines:
        print(line)

    print(f"\nTotal hours: {round(total_hours, 2)}")

    # Copy to clipboard (multi-line cell for Google Sheets)
    # clipboard_content = "\n".join(output_lines + [f"Total ({round(total_hours, 2)})"])
    clipboard_content = "\n".join(output_lines)
    pyperclip.copy(clipboard_content)
    print("\n✅ Output copied to clipboard with line breaks!")
    print("📋 Paste into Google Sheets by entering the cell (double-click or F2) before pasting.\n")

    # --- NEW FEATURE: Print "Yesterday" task list ---
    print("Yesterday")
    for task in task_order:
        print(f"• {task}")  # Slack-friendly bullet point


if __name__ == "__main__":
    main()
