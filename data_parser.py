"""TODO"""

import csv


def get_app_data(samples_tsv_path, transmissions_tsv_path):
    """TODO"""
    app_data = {
        "samples": {},
        "transmissions": {}
    }
    with open(samples_tsv_path) as fp:
        reader = csv.DictReader(fp, delimiter="\t")
        for row in reader:
            app_data["samples"][row.pop("sample_id")] = row
    with open(transmissions_tsv_path) as fp:
        reader = csv.DictReader(fp, delimiter="\t")
        for row in reader:
            app_data["transmissions"][row.pop("transmission_id")] = row
    return app_data
