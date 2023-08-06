import os
import re
from distutils.core import setup

with open(os.path.join(os.path.dirname(__file__), "pyproject.toml"), "r") as f:
    project_info = f.read()

    regex = r"version = \"(.*)\""

    __version__ = re.findall(regex, project_info)[0]

download_url = "https://github.com/alesanmed-educational-projects/covid-data/archive/refs/tags/{}.tar.gz".format(__version__)

setup(
  name = 'covid_data',
  packages = ['covid_data'],
  version = __version__,
  license='The Unlicense',
  description = 'Data loader part of the mid-project for the Data Science bootcamp from Core Code School',
  author = 'alesanchez',
  author_email = 'hi@alesanchez.es',
  url = 'https://github.com/alesanmed-educational-projects/core-data-covid-project',
  download_url = download_url,
  keywords = ['covid', 'core'],
  install_requires=[
      'pandas',
      'beautifulsoup4',
      'click',
      'python',
      'requests',
      'psycopg2',
      'Unidecode',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'License :: OSI Approved :: The Unlicense (Unlicense)',
    'Programming Language :: Python :: 3.9',
  ],
)
