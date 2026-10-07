# workshop_setup.py

import sys
import subprocess
import urllib.request
import zipfile
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules

DATA_URL = (
    "https://www.dropbox.com/scl/fi/"
    "5sk2tw3vyyueuvznbwk1l/data.zip"
    "?rlkey=j6d7hrcnrdujj25u87ojc7r7i"
    "&dl=1"
)

def configure_backend():

    from IPython import get_ipython

    ip = get_ipython()

    if ip is None:
        return

    if IN_COLAB:

        from google.colab import output

        output.enable_custom_widget_manager()

        ip.run_line_magic(
            "matplotlib",
            "widget",
        )

        print(
            "Colab widget support enabled"
        )

    else:

        ip.run_line_magic(
            "matplotlib",
            "qt",
        )

        print(
            "Qt backend enabled"
        )


def install_requirements(root):

    if not IN_COLAB:
        return

    req_file = root / "requirements.txt"

    if not req_file.exists():

        raise FileNotFoundError(
            f"Could not find requirements.txt at {req_file}"
        )

    print(
        "Installing workshop requirements..."
    )

    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-q",
            "-r",
            str(req_file),
        ],
        check=True,
    )

    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-q",
            "ipympl",
            "ipywidgets",
        ],
        check=True,
    )

def workshop_data_present(
    required_files,
):

    return all(
        f.exists()
        for f in required_files
    )

def download_workshop_data(
    workshop_dir,
    data_dir,
):

    workshop_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    data_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    zip_path = workshop_dir / "data.zip"

    print(
        "Downloading workshop data..."
    )

    urllib.request.urlretrieve(
        DATA_URL,
        zip_path,
    )

    print(
        "Extracting workshop data..."
    )

    with zipfile.ZipFile(
        zip_path,
        "r",
    ) as zf:

        zf.extractall(data_dir)

    zip_path.unlink(
        missing_ok=True
    )

    fits_files = sorted(
        data_dir.glob("*.fits")
    )

    print(
        f"Workshop data ready "
        f"({len(fits_files)} FITS files found)."
    )

def setup_workshop(
    root,
    workshop_name="USO_Vikram_2026_Oct",
):

    install_requirements(root)

    configure_backend()

    workshop_dir = (
        root
        / "workshops"
        / workshop_name
    )

    data_dir = (
        workshop_dir
        / "data"
    )

    required_files = [
        data_dir / "SUTNB01.fits",
        data_dir / "ROI_SUT_NB01.fits",
    ]

    if workshop_data_present(
        required_files
    ):

        fits_files = sorted(
            data_dir.glob("*.fits")
        )

        print(
            f"Workshop data already available "
            f"({len(fits_files)} FITS files found)."
        )

    else:

        print(
            "Workshop data missing or incomplete."
        )

        download_workshop_data(
            workshop_dir,
            data_dir,
        )

    return (
        workshop_dir,
        data_dir,
    )

