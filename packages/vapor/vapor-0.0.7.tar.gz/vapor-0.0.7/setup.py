# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vapor']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'boto3>=1.18,<2.0',
 'cfn-flip>=1.2.3,<2.0.0',
 'cfn-lint>=0.53.0,<0.54.0']

entry_points = \
{'console_scripts': ['vapor-import = vapor.__main__:import_']}

setup_kwargs = {
    'name': 'vapor',
    'version': '0.0.7',
    'description': 'Django ORM meets Cloudformation',
    'long_description': '# vapor\n\n![build](https://github.com/xiaket/vapor/workflows/build/badge.svg)\n![PyPI version](https://badge.fury.io/py/vapor.svg)\n![Coverage](https://coveralls.io/repos/github/xiaket/vapor/badge.svg)\n![license](https://img.shields.io/pypi/l/vapor)\n\nVapor is an alternative way to write and manage your cloudformation stacks. Think of CDK, but with a promise to generate a template that is easy to understand and easy to manage. Also, if you are familiar with Django ORM, the way we define resources is really similar to how we define models in Django.\n',
    'author': 'Kai Xia',
    'author_email': 'kaix+github@fastmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xiaket/vapor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
