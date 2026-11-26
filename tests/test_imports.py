"""Ensure scaffold modules import without data, weights or optional extras."""

import importlib
import pkgutil

import lordosis


def test_all_package_modules_import() -> None:
    """Every module is importable without executing its deferred workflow."""
    modules = list(pkgutil.walk_packages(lordosis.__path__, prefix="lordosis."))
    assert modules
    for module in modules:
        importlib.import_module(module.name)
