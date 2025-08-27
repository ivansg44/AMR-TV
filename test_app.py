from base64 import b64encode
from os import path

from data_parser import get_app_data


def test_kpc3_ecl719_snapshot(snapshot):
    with open(path.join("kpc3_data", "kpc3_ecl719_data.csv"), "rb") as fp:
        data_b64str = b64encode(fp.read())
    with open(path.join("kpc3_data", "kpc3_ecl719_config.json"), "rb") as fp:
        config_b64str = b64encode(fp.read())
    with open(path.join("kpc3_data", "kpc3_ecl719_snp_matrix.csv"), "rb") as fp:
        matrix_b64str = b64encode(fp.read())
    kpc3_ecl719_parsed_data = get_app_data(data_b64str,
                                           config_b64str,
                                           matrix_b64str)
    assert kpc3_ecl719_parsed_data == snapshot
