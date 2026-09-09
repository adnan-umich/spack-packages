# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.r import RCollectivePackage

from spack.package import *


class Rtidyverse(RCollectivePackage):
    """Easily Install and Load the Tidyverse.

    The tidyverse is a set of packages that work in harmony because they share
    common data representations and API design. This package is designed to
    make it easy to install and load multiple tidyverse packages in a single
    step."""

    has_code = False
    metalist = {
    "2.0.0_R4.6.1": [('r', '4.6.1'), ("r-tidyverse", "2.0.0")],
    "2.0.0_R4.5.3": [('r', '4.5.3'), ("r-tidyverse", "2.0.0")],
    }

    for key in metalist.keys():
        version(key)
        for pairing in metalist[key]:
             depends_on(f"{pairing[0]}@{pairing[1]}", when=f"@{key}", type="run")
    
    depends_on("c", type="build")
    depends_on("cxx", type="build")
