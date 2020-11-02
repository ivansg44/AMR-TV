"""Temporary script for converting tsv files into JSON."""

import csv
import json
import os


def parse_amr_genotypes(tsv_field):
    """Convert amr genotypes tsv field to required list."""
    return [x.split("=")[0] for x in tsv_field.split(",")]


with os.scandir() as it:
    for entry in it:
        if not entry.name.endswith(".tsv") or not entry.is_file():
            continue
        with open(entry.path) as fp:
            reader = csv.reader(fp, delimiter="\t")
            next(reader, None)
            isolates_fixture = []
            for row in reader:
                isolates_fixture.append(
                    {
                        "model": "isolate.isolate",
                        "fields": {
                            "organism_group": row[0],
                            "isolate": row[4],
                            "create_date": row[5],
                            "location": row[6],
                            "isolation_source": row[7],
                            "host": row[9],
                            "amr_genotypes": parse_amr_genotypes(row[15])
                        }
                    }
                )
            with open(entry.name.split('.')[0] + ".json", "w") as fp_two:
                json.dump(isolates_fixture, fp_two)
