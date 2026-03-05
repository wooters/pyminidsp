"""Minimal setup.py to enable CFFI extension compilation during pip install."""

from setuptools import setup

setup(
    cffi_modules=["pyminidsp/_build_minidsp.py:ffibuilder"],
)
