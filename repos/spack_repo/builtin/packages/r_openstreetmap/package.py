# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.r import RPackage

from spack.package import *


class ROpenstreetmap(RPackage):
    """Accesses high resolution raster maps using the OpenStreetMap protocol.
       Dozens of road, satellite, and topographic map servers are directly supported.
       Additionally raster maps may be constructed using custom tile servers.
       Maps can be plotted using either base graphics, or ggplot2.
       This package is not affiliated with the OpenStreetMap.org mapping project."""

    cran = "OpenStreetMap"

    license("GPL-2.0-only", checked_by="theAeon")

    version("0.4.1", sha256="e5756527d232c90eaae4c374c8246d0e15c018c78fb9dd9b297b05c60d07d39c")
    version("0.4.0", sha256="6e36831eabb6a2bf8783255cc7af0ed62fef72ce33756711bb57e630c6f00347")
    version("0.3.4", sha256="61a0c711d91e61b8e77c0693112798e5005bafd3154ba29632d6a0d82909db4f")
    version("0.3.3", sha256="ff8611debb3ac3e2842c72ed5d23ea877ed23c5aedbd7f76a13df10db06f3b25")
    version("0.3.2", sha256="56feb0ada34fbc423dd2cb449dd9e5ad80b6444643b4aa53ccd7d3bdc8f55fb3")
    version("0.3.1", sha256="ebbbf3d0be16317c917ad3fa5efdddf5c6ccecc1dfeb6ad4a263e1b7348e3d01")
    version("0.3", sha256="a6a2ab00f5bbec1b89d0a32f530803060e570e661c890dfca896fb7b148dca79")
    version("0.2", sha256="18148e3f48b7d6c5e68c85185763b186091f30026c8be9e8cc0d8576cc3b6794")

    with default_args(type=("build", "run")):
        depends_on("r@4.2.0:", when="@0.4.1:")
        depends_on("r-ggplot2@0.9.0:", when="@0.4.1:")
        depends_on("r-rjava", when="@0.4.1:")
        depends_on("r-raster", when="@0.4.1:")
        depends_on("r-sp", when="@0.4.1:")
        depends_on("r-stars")
        depends_on("r-tmaptools")
        depends_on("r-trajectories")
