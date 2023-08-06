# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mo_parsing', 'mo_sql_parsing']

package_data = \
{'': ['*']}

install_requires = \
['mo-dots==4.22.21108',
 'mo-future==3.147.20327',
 'mo-imports==3.149.20327',
 'mo-kwargs==4.22.21108',
 'mo-logs==4.23.21108']

setup_kwargs = {
    'name': 'mo-sql-parsing',
    'version': '0.1.2',
    'description': 'Extract Parse Tree from SQL',
    'long_description': '# mo-sql-parser\n\nForked from [klahnakoski/mo-sql-parsing](https://github.com/klahnakoski/mo-sql-parsing).\n',
    'author': 'DataLabs',
    'author_email': 'time.dataanalytics.datalabs@compasso.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/doraproject/mo-sql-parsing',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
