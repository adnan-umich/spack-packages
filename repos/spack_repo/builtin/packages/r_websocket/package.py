# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.r import RPackage

from spack.package import *


class RWebsocket(RPackage):
    """WebSocket client library for R."""

    cran = "websocket"

    version("1.4.4", sha256="9fcd00271e461ec9deda4aef83155f9f8c9125490123fc11121df48e11f4142e")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("openssl@1.0.2:")
    depends_on("r-r6", type=("build", "run"))
    depends_on("r-later@1.2.0:", type=("build", "run"))
    depends_on("r-cpp11", type=("build", "run"))
    depends_on("r-asioheaders", type=("build", "run"))
