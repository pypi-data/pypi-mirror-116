# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prefect_geopandas_serializer']

package_data = \
{'': ['*']}

install_requires = \
['geopandas>=0.9.0,<0.10.0', 'prefect>=0.15.3,<0.16.0', 'pyarrow>=5.0.0,<6.0.0']

setup_kwargs = {
    'name': 'prefect-geopandas-serializer',
    'version': '0.1.0',
    'description': 'PandasSerializer adapted for GeoPandas',
    'long_description': None,
    'author': 'Rowan Molony',
    'author_email': 'rowan.molony@codema.ie',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
