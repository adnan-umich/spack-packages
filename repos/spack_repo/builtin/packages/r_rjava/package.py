# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.r import RPackage

from spack.package import *


class RRjava(RPackage):
    """Low-level interface between R and Java."""

    cran = "rJava"

    version("1.0-18", sha256="a4db39f39cdb05dbfa667ea6e4db9fd3402f395d9ec1a50a18d0397927f1f552")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("r@3.6.0:+java", type=("build", "run"))
    depends_on("java@1.4:", type=("build", "run"))
