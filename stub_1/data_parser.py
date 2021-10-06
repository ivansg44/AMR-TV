import csv
from datetime import datetime


def get_app_data(sample_csv_path):
    sample_data_dict = get_sample_data_dict(sample_csv_path)

    date_list = [v["date"] for v in sample_data_dict.values()]
    date_x_vals_dict = {
        e: i+1 for i, e in enumerate(dict.fromkeys(sorted(date_list)))
    }

    location_list = [v["location"] for v in sample_data_dict.values()]
    location_y_vals_dict = {
        e: i+1 for i, e in enumerate(dict.fromkeys(sorted(location_list)))
    }

    app_data = {
        "main_fig_xaxis_range":
            [0.5, len(date_x_vals_dict) + 0.5],
        "main_fig_xaxis_tickvals":
            list(range(1, len(date_x_vals_dict) + 1)),
        "main_fig_xaxis_ticktext":
            list(date_x_vals_dict.keys()),
        "main_fig_yaxis_tickvals":
            list(range(1, len(location_y_vals_dict) + 1)),
        "main_fig_yaxis_ticktext":
            list(location_y_vals_dict.keys()),
        "main_fig_nodes_x":
            [date_x_vals_dict[e] for e in date_list],
        "main_fig_nodes_y":
            [location_y_vals_dict[e] for e in location_list]
    }

    return app_data


def get_sample_data_dict(sample_csv_path):
    sample_data_dict = {}
    with open(sample_csv_path) as fp:
        next(fp)
        reader = csv.DictReader(fp)
        for row in reader:
            sample_id = row["Sample ID / Isolate"]
            if not sample_id:
                continue

            datetime_obj =\
                datetime.strptime(row["Date of collection"], "%B %Y")
            datetime_iso_str = datetime_obj.strftime("%G-%m-%d")

            sample_data_dict[sample_id] = {
                "patient_id": row["Patient ID"],
                "location": row["Location"],
                "date": datetime_iso_str,
                "organism": row["Organism"],
                "mlst": row["F1: MLST type"],
                "gene": row["Resitance gene type"],
                "homozygous_snps": row["SNPs_homozygous"],
                "left_flanks": row["Left_flanks"],
                "right_flanks": row["Right_flanks"],
                "mash_neighbour_cluster": row["mash_neighbor_cluster"],
                "replicon_types": row["rep_type(s)"],
                "relaxase_types": row["relaxase_type(s)"],
                "predicted_mobility": row["PredictedMobility"]
            }
    return sample_data_dict
