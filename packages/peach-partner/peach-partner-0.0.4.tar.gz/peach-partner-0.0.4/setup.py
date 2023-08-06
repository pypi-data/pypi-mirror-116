# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['peach_partner']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'peach-partner',
    'version': '0.0.4',
    'description': 'Peach Partner Library is a platform agnostic Python package to help integrating PeachPayments with their partners.',
    'long_description': '# Peach Partner Library\n\n## Overview\n\n**Peach Partner Library** is a platform agnostic Python package to help integrating PeachPayments with their partners.\n\n\n**Documentation**:\n\n**Source Code**: https://gitlab.com/peachpayments/peach-partner-python/\n\n---\n\n## Usage\nPackage requires Python 3.9+\n\n### Installation\n```sh\n# pip\n$ pip3 install peach-partner\n```\n```sh\n# poetry\n$ poetry add peach-partner\n```\n### Result codes\n```python\nfrom peach_partner.result_codes import result_codes\n\nresult_codes.TRANSACTION_SUCCEEDED.code == "000.000.000"\nresult_codes.get("000.000.000").name == "TRANSACTION_SUCCEEDED"\nresult_codes.get("000.000.000").description == "Transaction succeeded"\n```\n### Field validation\nTODO\n### Authentication\nTODO\n',
    'author': 'Peach Payments',
    'author_email': 'support@peachpayments.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
