from datetime import datetime
from decimal import Decimal
import sys
import pandas as pd


class Entry:
    def __init__(self, week, date, hours, task, category):
        self.week = week
        self.date = datetime.strptime(date, '%m/%d/%Y').date()
        self.hours = Decimal(hours)
        self.task = task
        self.category = category


def print_usage_and_exit():
    print("usage: python csv_converter.py <csv_file>")
    sys.exit()


def validate_args(args):
    if len(args) != 2:
        print("Not enough or too many arguments")
        print_usage_and_exit()


def _validate_headers(input_file):
    df = pd.read_csv(input_file, nrows=1)
    expected_header_fields = ["Week", "Date", "Hours", "Task", "Category"]
    actual_headers = []
    for index, row in df.iterrows():  # we shouldn't need a for loop here. There has to be a better way
        actual_headers = list(row.keys())

    if expected_header_fields == actual_headers:
        print("headers match")
    else:
        print(f"actual header fields: {actual_headers}")
        print(f"Error: header fields expected to be: {','.join(expected_header_fields)}")
        print_usage_and_exit()


def read_file(input_file):
    weeks = []
    df = pd.read_csv(input_file, sep=",")

    category_to_entry_list = {}
    for index, raw_line in df.iterrows():
        entry = Entry(raw_line["Week"], raw_line["Date"], raw_line["Hours"], raw_line["Task"],
                      raw_line["Category"])
        if category_to_entry_list.get(entry.category):
            category_to_entry_list[entry.category].append(entry)
        else:
            category_to_entry_list[entry.category] = [entry]

    return category_to_entry_list


def main():
    print(f"CSV converter to invoice-formatted fields")
    validate_args(sys.argv)
    _validate_headers(sys.argv[1])
    category_to_entry_list = read_file(sys.argv[1])
    print("----")
    total_hours = 0
    for category in sorted(category_to_entry_list.keys()):
        print(f"{category}")
        entries = category_to_entry_list[category]
        hours_per_category = 0
        for entry in entries:
            print(f"{entry.task} ({entry.date.strftime('%B %d')} - {entry.hours} hours)")
            total_hours += entry.hours
            hours_per_category += entry.hours

        print(f"\nhours for category: {hours_per_category}")

        print("----")

    print(f"\ntotal hours: {total_hours}")


if __name__ == "__main__":
    main()