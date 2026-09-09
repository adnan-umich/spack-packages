# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.r import RCollectivePackage

from spack.package import *


class Rgeospatial(RCollectivePackage):
    """Easily Install and Load Geospatial Packages in R.

    This package provides an easy way to install and load multiple geospatial
    packages in R, ensuring that all necessary dependencies are correctly
    configured."""

    has_code = False
    metalist = {
    "1.5-18_R4.6.1": [('r', '4.6.1'), ("r-geosphere", "1.5-18"), ("r-chromote", "0.5.1"),
                     ("r-leafem", "0.2.3"), ("r-leaflet", "2.2.2"), ("r-satellite", "1.0.5"),
                     ("r-tidyverse", "2.0.0"), ("r-s2", "1.1.12"), ("r-terra", "1.9-11"),
                     ("r-foreign", "0.8-87"), ("r-raster", "3.6-26"), ("r-sfnetworks", "0.6.6"),
                     ("r-spatstat", "3.1-1"), ("r-mapproj", "1.2.11"), ("r-openstreetmap", "0.4.1"),
                     ("r-gdalutilities", "1.2.5"), ("r-mapview", "2.11.2"), ("r-tigris", "2.1"),
                     ],
    "1.5-18_R4.5.3": [('r', '4.5.3'), ("r-geosphere", "1.5-18"), ("r-chromote", "0.5.1"),
                     ("r-leafem", "0.2.3"), ("r-leaflet", "2.2.2"), ("r-satellite", "1.0.5"),
                     ("r-tidyverse", "2.0.0"), ("r-s2", "1.1.12"), ("r-terra", "1.9-11"),
                     ("r-foreign", "0.8-87"), ("r-raster", "3.6-26"), ("r-sfnetworks", "0.6.6"),
                     ("r-spatstat", "3.1-1"), ("r-mapproj", "1.2.11"), ("r-openstreetmap", "0.4.1"),
                     ("r-gdalutilities", "1.2.5"), ("r-mapview", "2.11.2"), ("r-tigris", "2.1"),
                     ],
    }

    for key in metalist.keys():
        version(key)
        for pairing in metalist[key]:
             depends_on(f"{pairing[0]}@{pairing[1]}", when=f"@{key}", type="run")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("gdal")
    depends_on("proj")
    depends_on("geos")
    #depends_on("pkgconfig", type="build")
    depends_on('netcdf-fortran')
    depends_on('hdf5+hl+cxx+fortran')
    depends_on("java", type=("build", "run"))
