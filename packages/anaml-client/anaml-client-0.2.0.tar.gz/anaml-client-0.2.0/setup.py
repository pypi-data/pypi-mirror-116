#
# Copyright 2020 Simple Machines Pty Ltd - All Rights Reserved.
#
# This file is part of Anaml.
#
# Unauthorized copying and/or distribution of this file, via any medium
# is strictly prohibited.
#

from setuptools import setup, find_namespace_packages
import subprocess
import re


# Get version number from git tags
rev_parse = subprocess.run(['git', 'describe'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
status = subprocess.run(['git', 'status', '--porcelain'], check=True, stdout=subprocess.PIPE, universal_newlines=True)

if rev_parse.returncode == 0 and rev_parse.returncode == 0:
    modified = len(status.stdout) > 0
    if modified:
        flag = ".m"
    else:
        flag = ""
    version = (rev_parse.stdout.strip() + flag).replace("release-v", "")
else:
    print("Unable to determine version number from git tags")
    exit(1)
# Change git describe output to be valid for Python (PEP 400)
version = re.sub(pattern="-([0-9]+)-([a-z0-9]+)", repl="+\\1.\\2", string=version)

# As far as I can tell, there's no other way to access this from within the module other than
# by munging the source code at install time.
with open("src/anaml_client/version.py", "w") as f:
    f.write(f'"""Version metadata for the package."""\n\n__version__ = "{version}"\n')

setup(
    name="anaml-client",
    version=version,
    author="Simple Machines",
    author_email="hello@simplemachines.com.au",
    classifiers=['Programming Language :: Python :: 3', 'Operating System :: OS Independent',
                 'License :: Other/Proprietary License'],
    description="Python SDK for Anaml",
    license="Copyright 2020 Simple Machines Pty Ltd. All Rights Reserved",
    url="https://anaml.com",
    # adding packages
    packages=find_namespace_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        "pandas", "jsonschema", "requests", "matplotlib", "numpy", "scipy",
        "seaborn", "isodate"
    ],
    test_suite="tests",
    extras_require={"testing": [
        "flake8", "hypothesis", "pytest"
    ]},
)
