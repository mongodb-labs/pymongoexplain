import os

from setuptools import setup, find_packages

with open('README.rst', 'rb') as f:
    LONG_DESCRIPTION = f.read().decode('utf8')

# Single source the version.
version_file = os.path.realpath(os.path.join(
    os.path.dirname(__file__), 'pymongoexplain', 'version.py'))
version = {}
with open(version_file) as fp:
    exec(fp.read(), version)

setup(
    name="pymongoexplain",
    version=version['__version__'],
    description="Explainable CRUD API for PyMongo",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(exclude=['test']),
    author="Julius Park",
    url="https://github.com/mongodb-labs/pymongoexplain",
    keywords=["mongo", "mongodb", "pymongo"],
    test_suite="test",
    entry_points={
        'console_scripts': [
            'pymongoexplain=pymongoexplain.cli_explain:cli_explain'],
    },
    tests_require=["pymongo>=3.11"],
    install_requires=['pymongo>=3.11'],
    python_requires='>=3.5',
    license="Apache License, Version 2.0",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Database"]
)
