from base64 import b64encode
from pathlib import Path

from syrupy.extensions.json import JSONSnapshotExtension

from amr_tv.data_parser import get_app_data

KPC3_DATA_DIR = Path(__file__).parent.parent / "data" / "kpc3_data"

def test_kpc3_ecl719_snapshot(snapshot):
    data_b64str = b64encode(
        (KPC3_DATA_DIR / "kpc3_ecl719_data.csv").read_bytes()
    )
    config_b64str = b64encode(
        (KPC3_DATA_DIR / "kpc3_ecl719_config.json").read_bytes()
    )
    matrix_b64str = b64encode(
        (KPC3_DATA_DIR / "kpc3_ecl719_snp_matrix.csv").read_bytes()
    )
    actual = get_app_data(data_b64str, config_b64str, matrix_b64str)
    assert actual == snapshot.use_extension(JSONSnapshotExtension)


def test_kpc3_snapshot(snapshot):
    data_b64str = b64encode(
        (KPC3_DATA_DIR / "kpc3_data.csv").read_bytes()
    )
    config_b64str = b64encode(
        (KPC3_DATA_DIR / "kpc3_config.json").read_bytes()
    )
    actual = get_app_data(data_b64str, config_b64str)
    assert actual == snapshot.use_extension(JSONSnapshotExtension)
