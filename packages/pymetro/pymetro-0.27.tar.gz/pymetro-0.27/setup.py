from setuptools import setup, Extension
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="pymetro",
    packages=["pymetro"],
    version="0.27",
    license="GPL-3.0",
    description="A library for formatting numbers according to the metric system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Abdulrhman-AIG, baselkorj",
    author_email="abdalrhman.ib1998@gmail.com, baselanwarkorj@gmail.com",
    url="https://github.com/baselkorj/pymetro",
    download_url="https://github.com/user/pymetro/archive/pymetro_v02.tar.gz",
    keywords=["Units", "Metric", "Scientific Notation", "SI"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
