#!/usr/bin/env python3

import csv
import sqlite3
import argparse
import sys
import os


def main() -> None:
    parser = argparse.ArgumentParser(prog=sys.argv[0], description="Load CSV data into DB")
    parser.add_argument(
        "--db-file",
        metavar="<DB FILE PATH>",
        help="Path to database",
        required=True,
    )

    args = parser.parse_args()
    conn = sqlite3.connect(args.db_file)

    my_dir = os.path.realpath(os.path.dirname(os.path.realpath(__file__)))

    for file in os.listdir(my_dir):
        if not file.endswith(".csv"):
            continue

        table = os.path.splitext(file)[0]
        cur = conn.cursor()
        rows = []
        fields = None

        with open(f"{my_dir}/{file}", newline="") as fd:
            reader = csv.DictReader(fd)
            fields = reader.fieldnames
            for row in reader:
                rows.append(row)

        field_dict = {}
        for field in fields:
            (name, ftype) = field.split(":")
            name = name.lower().replace(" ", "_")
            field_dict[name] = ftype

        cur.execute("""CREATE TABLE %s (%s)""" % (table, ",".join([f"{f} {t}" for f, t in field_dict.items()])))

        for row in rows:
            cur.execute("""INSERT INTO %s VALUES (%s)""" % (table, ",".join([f"'{v}'" for v in row.values()])))

        conn.commit()
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
