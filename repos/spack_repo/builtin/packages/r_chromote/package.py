# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.r import RPackage

from spack.package import *


class RChromote(RPackage):
    """An implementation of the 'Chrome DevTools Protocol', for controlling a headless Chrome web browser."""


    cran = "chromote"


    license("MIT", checked_by="theAeon")

    version("0.5.1", sha256="b0caa76507a2dea3c524c84d99ca0ac77eb8b46b60adc02fbc80c67741b354b5")
    version("0.5.0", sha256="8b46297f38399701e9eec36d35f57adf79a6bf3372013bb7a27946f34e6a90e7")
    version("0.4.0", sha256="44e9ea99b15328146aa3d5ac25c4ecbbbfaf1bfa59c1c33fd01e3e1913dfe51d")
    version("0.3.1", sha256="a233563a0015b92cb430489d37d2ae2e0dc4374c00dd44dac756b5a507cf9d47")
    version("0.3.0", sha256="0f8480692f86626c94e8035061eb890143260bbc874e0609c79730a369cd6b56")
    version("0.2.0", sha256="a376af67a2f9e6684425e6463f1b3a488e1a712d11b48f3b7d0f9863d2410875")
    version("0.1.2", sha256="c0117f09b8dbad4a5fcfd09911ab8662ad4a830eef1344787b78e4770886d8ba")
    version("0.1.1", sha256="f89427addeb2a990906a2ef541d2690ac69de91ec38a094feb4560b6ada64929")
    version("0.1.0", sha256="3edc1c349352bdcb5fx3974c350668473440809badf70e11e29b41c5ede67a06c")

    with when("@0.5.1:"):
        with default_args(type=("build", "run")):
            depends_on("r-cli")
            depends_on("r-curl")
            depends_on("r-fastmap")
            depends_on("r-jsonlite")
            depends_on("r-later@1.1.0:")
            depends_on("r-magrittr")
            depends_on("r-processx")
            depends_on("r-promises@1.1.1:")
            depends_on("r-r6")
            depends_on("r-rlang@1.1.0:")
            depends_on("r-websocket@1.2.0:")
            depends_on("r-withr")
            depends_on("r-zip")
