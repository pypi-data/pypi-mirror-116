# neuralmagic: no copyright
# flake8: noqa
__all__ = ["__version__", "version", "version_major", "version_minor", "version_bug", "version_build", "version_major_minor", "optimized", "is_release", "revision", "splash", "is_nightly", "build_date"]
__version__ = '0.6.1'

version = __version__
version_major, version_minor, version_bug, version_build = version.split(".") + (
    [None] if len(version.split(".")) < 4 else []
) # handle conditional for version being 3 parts or 4 
version_major_minor = f"{version_major}.{version_minor}"
optimized = 1
is_release = 1
is_nightly = 0
revision = '1e0f56a7'
splash = 'DeepSparse Engine, Copyright 2021-present / Neuralmagic, Inc. version: 0.6.1 (1e0f56a7) (release) (optimized)'
build_date = '20210810'
