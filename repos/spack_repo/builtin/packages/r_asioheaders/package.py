# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.r import RPackage

from spack.package import *


class RAsioheaders(RPackage):
    """Asio C++ header files for R packages."""

    cran = "AsioHeaders"

    version("1.30.2-1", sha256="1be43b48a4cc704ef84b5673b4fc78323709fd0d61c18dbd364ac89a38e2ab31")


