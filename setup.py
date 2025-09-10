"""Данный сетап нужен для обнаружения __init__.py файлов для установления везде абсолютных импортов"""

from setuptools import setup, find_packages

setup(
    name="CoinKeeper API",
    version="0.1.0",
    packages=find_packages(),
)
