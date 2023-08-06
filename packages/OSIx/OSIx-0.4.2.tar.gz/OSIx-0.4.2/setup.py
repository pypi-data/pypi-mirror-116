import io
import os

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'OSIx'
DESCRIPTION = 'Open Source Intelligence eXplorer.'
URL = 'https://github.com/guibacellar/OSIx/'
AUTHOR = 'Th3 0bservator'
EMAIL = 'th30bservator@gmail.com'
REQUIRES_PYTHON = '>=3.7.6'
VERSION = '0.4.2'

# What packages are optional?
EXTRAS = {
}

here = os.path.abspath(os.path.dirname(__file__))

# What packages are required for this module to be executed?
try:
    with io.open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
        requirements_data = f.read()
except FileNotFoundError:
    requirements_data = ''
REQUIRED = [req for req in requirements_data.split('\n') if '==' in req and 'tox' not in req and 'pytest' not in req]
print(REQUIRED)

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README_PYPI.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Where the magic happens:
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    keyword=[
        "CyberSecurity",
        "Investigation",
        "OSINT",
        "OpenSourceIntelligence",
        "Tool"
    ],
    packages=find_packages(
        exclude=["tests", "*.tests", "*.tests.*", "tests.*", "venv.*"],
        where="."
    ),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='Apache-2.0',
    classifiers=[
        'Environment :: Console',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Security',
        'Topic :: Utilities'
    ],
    project_urls={
        'Bug Tracker': 'https://github.com/guibacellar/OSIx/issues',
        'Documentation': 'https://github.com/guibacellar/OSIx/blob/develop/README.md',
        'Source Code': 'https://github.com/guibacellar/OSIx/'
    }
)
