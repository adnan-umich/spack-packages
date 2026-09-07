# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import shutil
from typing import Iterable, List, Optional, Tuple

from spack.package import (
    BuilderWithDefaults,
    ClassProperty,
    HeaderList,
    LibraryList,
    Prefix,
    Spec,
    build_system,
    classproperty,
    depends_on,
    extends,
    join_path,
    mkdirp,
    register_builder,
    tty,
    variant,
    when,
)

from .generic import GenericBuilder, Package


class RBuilder(GenericBuilder):
    """The R builder provides a single phase that can be overridden:

        1. :py:meth:`~.RBuilder.install`

    It has sensible defaults, and for many packages the only thing
    necessary will be to add dependencies.
    """

    #: Names associated with package methods in the old build-system format
    package_methods: Tuple[str, ...] = (
        "configure_args",
        "configure_vars",
    ) + GenericBuilder.package_methods

    def configure_args(self):
        """Arguments to pass to install via ``--configure-args``."""
        return []

    def configure_vars(self):
        """Arguments to pass to install via ``--configure-vars``."""
        return []

    def install(self, pkg, spec, prefix):
        """Installs an R package."""
        mkdirp(pkg.module.r_lib_dir)

        config_args = self.configure_args()
        config_vars = self.configure_vars()

        args = ["--vanilla", "CMD", "INSTALL"]

        if config_args:
            args.append(f"--configure-args={' '.join(config_args)}")

        if config_vars:
            args.append(f"--configure-vars={' '.join(config_vars)}")

        args.extend([f"--library={pkg.module.r_lib_dir}", self.stage.source_path])

        pkg.module.R(*args)


def _homepage(cls: "RPackage") -> Optional[str]:
    if cls.cran:
        return f"https://cloud.r-project.org/package={cls.cran}"
    elif cls.bioc:
        return f"https://bioconductor.org/packages/{cls.bioc}"
    return None


def _urls(cls: "RPackage") -> List[str]:
    if cls.cran:
        return [
            f"https://cran.r-project.org/src/contrib/{cls.cran}_{str(list(cls.versions)[0])}.tar.gz",
            f"https://cran.r-project.org/src/contrib/Archive/{cls.cran}/{cls.cran}_{str(list(cls.versions)[0])}.tar.gz",
        ]
    return []


def _list_url(cls: "RPackage") -> Optional[str]:
    if cls.cran:
        return f"https://cran.r-project.org/src/contrib/Archive/{cls.cran}/"
    return None


def _git(cls: "RPackage") -> Optional[str]:
    if cls.bioc:
        return f"https://git.bioconductor.org/packages/{cls.bioc}"
    return None


class RPackage(Package):
    """Specialized class for packages that are built using R.

    For more information on the R build system, see:
    https://stat.ethz.ch/R-manual/R-devel/library/utils/html/INSTALL.html
    """

    # package attributes that can be expanded to set the homepage, url,
    # list_url, and git values
    # For CRAN packages
    cran: Optional[str] = None

    # For Bioconductor packages
    bioc: Optional[str] = None

    GenericBuilder = RBuilder

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = "RPackage"

    extends("r")

    # needed for packages that need compiling
    depends_on("gmake", type="build", when="%c")
    depends_on("gmake", type="build", when="%cxx")
    depends_on("gmake", type="build", when="%fortran")

    homepage: ClassProperty[Optional[str]] = classproperty(_homepage)
    urls: ClassProperty[List[str]] = classproperty(_urls)
    list_url: ClassProperty[Optional[str]] = classproperty(_list_url)
    git: ClassProperty[Optional[str]] = classproperty(_git)


@register_builder("r_collective")
class RCollectiveBuilder(BuilderWithDefaults):
    """Create a unified R prefix from installed Spack packages."""

    phases = ("install",)

    def install(self, pkg, spec, prefix):
        r_spec = pkg.r_spec

        tty.info(
            "Creating R collective with {0}".format(
                r_spec.format("{name}@{version}/{hash:7}")
            )
        )

        mkdirp(prefix)

        #
        # Add R packages belonging to this R interpreter.
        #
        extensions = self._r_extensions(spec, r_spec)
        collective_lib_dir = self._collective_r_lib_dir(prefix, r_spec)
        mkdirp(collective_lib_dir)

        for extension in extensions:
            tty.info(
                "Adding {0}".format(
                    extension.format("{name}@{version}/{hash:7}")
                )
            )
            self._materialize_extension_library(extension, collective_lib_dir, r_spec)


        self._write_manifest(spec, prefix, r_spec, extensions)

    def _collective_r_lib_dir(self, prefix: Prefix, r_spec: Spec) -> str:
        return join_path(prefix, r_spec.package.r_lib_dir)

    def _materialize_extension_library(
        self, extension: Spec, collective_lib_dir: str, r_spec: Spec
    ) -> None:
        extension_lib_dir = join_path(extension.prefix, r_spec.package.r_lib_dir)
        if not os.path.isdir(extension_lib_dir):
            return

        for entry in sorted(os.listdir(extension_lib_dir)):
            src = join_path(extension_lib_dir, entry)
            dst = join_path(collective_lib_dir, entry)
            if os.path.isdir(src):
                shutil.copytree(src, dst, symlinks=True, dirs_exist_ok=True)
            elif os.path.islink(src):
                self._remove_path(dst)
                shutil.copy2(src, dst, follow_symlinks=False)
            else:
                self._remove_path(dst)
                shutil.copy2(src, dst)

    def _remove_path(self, path: str) -> None:
        if not os.path.lexists(path):
            return

        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
            return

        os.unlink(path)

    def _extension_deps(self, root_spec: Spec) -> Iterable[Spec]:
        if "+transitive" in root_spec:
            return root_spec.traverse(root=False, deptype=("link", "run"))

        return root_spec.dependencies(deptype=("link", "run"))

    def _r_extensions(self, root_spec: Spec, r_spec: Spec) -> List[Spec]:
        """Return R extensions belonging to this collective's R."""

        extensions = []

        for dep in self._extension_deps(root_spec):

            if dep.name == "r":
                continue

            if not dep.name.startswith("r-"):
                continue

            #
            # Only consider installed packages.
            #
            try:
                dep_pkg = dep.package
            except Exception:
                continue

            #
            # Python packages are extensions. Determine whether this package
            # extends R.
            #
            try:
                extendee_spec = dep_pkg.extendee_spec
            except Exception:
                extendee_spec = None

            if extendee_spec is None:
                continue

            if extendee_spec.name != "r":
                continue

            #
            # Make sure the extension belongs to the exact R instance
            # used by this collective.
            #
            try:
                extendee_r = dep["r"]
            except KeyError:
                continue

            if extendee_r.dag_hash() != r_spec.dag_hash():
                continue

            extensions.append(dep)

        return sorted(
            extensions,
            key=lambda x: (
                x.name,
                str(x.version),
                x.dag_hash(),
            ),
        )


    def _write_manifest(
        self,
        root_spec: Spec,
        prefix: Prefix,
        r_spec: Spec,
        extensions: List[Spec],
    ) -> None:
        """Record the exact contents of the collective."""

        metadata = join_path(prefix, ".spack-r-collective")
        mkdirp(metadata)

        manifest = join_path(metadata, "packages.txt")

        with open(manifest, "w", encoding="utf-8") as f:
            f.write("# Generated by RCollectiveBuilder\n")
            f.write(
                "# collective: "
                + root_spec.format("{name}@{version}/{hash}")
                + "\n\n"
            )

            f.write(
                r_spec.format("{name}@{version} /{hash} {prefix}")
                + "\n"
            )

            for dep in extensions:
                f.write(
                    dep.format("{name}@{version} /{hash} {prefix}")
                    + "\n"
                )


class RCollectivePackage(RPackage):
    """
    RCollectivePackage does not build R modules itself. Instead,
    it depends on normal Spack R packages and creates a unified prefix
    containing Python and all R extensions in its dependency DAG.

    Each dependency remains an independently installed Spack package.
    """

    build_system_class = "RCollectivePackage"

    default_buildsystem = "r_collective"

    build_system("r_collective")

    variant(
        "transitive",
        default=True,
        description="Include transitive R extension dependencies",
    )

    with when("build_system=r_collective"):
        extends("r")

    @property
    def r_spec(self) -> Spec:
        """R used by this collective."""
        r, *_ = self.spec.dependencies("r")
        return r

    @property
    def headers(self) -> HeaderList:
        return HeaderList([])

    @property
    def libs(self) -> LibraryList:
        return LibraryList([])
