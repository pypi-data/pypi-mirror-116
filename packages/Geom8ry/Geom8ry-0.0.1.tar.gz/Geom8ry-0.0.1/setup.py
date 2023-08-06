'''setup for Geom8ry
'''

from setuptools import setup, find_packages
from codecs import open
from os import path


# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

long_description = '''
# Geom8ry - Python Geom8ry Package

## Development Stage : 2 - Pre-Alpha 
## Warning : Unstable
Version: 0.0.1

Geom8ry is a python package for performing computational
geometry. Geom8ry can handle various 2D - geometrical constructs like Points, Lines, Line Segments,  Polygons, Circles,  Fourier Transforms, Matrices, Graphs, Triangulations, and  Polynomials, etc.

It's also a personal exercise in learning how to provide a high
quality python package:

- support of powerful tools like Delaunay Triangulations, FFTs, Inverse FFTs, Convex Hulls, and Fast Polynomial Multiplications
- appropriate use of exceptions and exception handling
- designing of useful base classes and methods
- high-quality documentation
- efficient implementation of algorithms and data structures
'''

version = "0.0.1"

# download_url = 'https://github.com/raje-ev/Geom8ry/archive/{}.tar.gz'

setup(name='Geom8ry',
      version=version,
      description='Geom8ry the python way.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/raje-ev/Geom8ry',
      # download_url=download_url.format(version),
      author="Rajeev Kumar",
      author_email="rajeevkumar.nitp@gmail.com",
      license='MIT',
      project_urls={
        "Bug Tracker": "https://github.com/raje-ev/Geom8ry/issues",
      },
      classifiers=['Development Status :: 2 - Pre-Alpha',
                   'Intended Audience :: Education',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: Scientific/Engineering :: Mathematics',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.6',
                   "Operating System :: OS Independent"],
      keywords='Geom8ry point circle line line segment triangle rectangle graph fft dft triangulation',
      package_dir={"": "src"},
      packages=find_packages(where="src"),
      python_requires=">=3.6",
      test_suite='Geom8ry.tests',
      install_requires=[],
      extras_require={},
      package_data={},
      data_files=[],
      )
