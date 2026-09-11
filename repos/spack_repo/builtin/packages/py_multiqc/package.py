# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyMultiqc(PythonPackage):
    """MultiQC aggregates results from bioinformatics analyses across
    many samples into a single report."""

    homepage = "https://multiqc.info"
    pypi = "multiqc/multiqc-1.35.tar.gz"

    maintainers("ewels", "vladsavelyev")

    license("GPL-3.0-only", checked_by="A_N_Other")

    version(
        "1.35",
        sha256="5a4aa6480e6def2f9c0af2893358bf7ec5c304d606ecf613cd25ddcd0e244e77",
    )

    # pyproject.toml:
    # requires-python = ">=3.9, !=3.14.1"
    depends_on("python@3.9:3.14.0,3.14.2:", type=("build", "run"))

    # [build-system]
    # requires = ["setuptools"]
    depends_on("py-setuptools", type="build")

    # [project.dependencies]
    depends_on("py-boto3", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
    depends_on("py-humanize", type=("build", "run"))
    depends_on("py-importlib-metadata", type=("build", "run"))
    depends_on("py-jinja2@3.0:", type=("build", "run"))

    # MultiQC still requires the old self-contained Kaleido 0.2.x backend.
    depends_on("py-kaleido@0.2.1", type=("build", "run"))

    depends_on("py-markdown", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-pillow@10:", type=("build", "run"))
    depends_on("py-plotly@5.18:", type=("build", "run"))
    depends_on("py-pyyaml@4:", type=("build", "run"))
    depends_on("py-rich@10:", type=("build", "run"))
    depends_on("py-rich-click", type=("build", "run"))
    depends_on("py-coloredlogs", type=("build", "run"))
    depends_on("py-spectra@0.0.10:", type=("build", "run"))
    depends_on("py-pydantic@2.7:", type=("build", "run"))
    depends_on("py-typeguard@4:", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-python-dotenv", type=("build", "run"))
    depends_on("py-natsort", type=("build", "run"))
    depends_on("py-tiktoken", type=("build", "run"))
    depends_on("py-jsonschema", type=("build", "run"))

    # Native Linux installs use:
    #   polars[rtcompat] >= 1.34.0
    #
    # Spack does not encode Python extras on depends_on(), so package the
    # required Polars dependency explicitly.
    depends_on("py-polars@1.34:", type=("build", "run"))

    # Parquet support
    depends_on("py-pyarrow", type=("build", "run"))
