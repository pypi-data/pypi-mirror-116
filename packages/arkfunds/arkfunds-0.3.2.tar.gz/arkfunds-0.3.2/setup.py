# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arkfunds']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.1,<2.0.0', 'requests>=2.26.0,<3.0.0']

extras_require = \
{'docs': ['Sphinx>=4.1.2,<5.0.0', 'sphinx-rtd-theme>=0.5.2,<0.6.0']}

setup_kwargs = {
    'name': 'arkfunds',
    'version': '0.3.2',
    'description': 'Python library for monitoring Ark Invest funds data.',
    'long_description': 'arkfunds-python\n===============\n\n.. image:: https://badge.fury.io/py/arkfunds.svg\n   :target: https://badge.fury.io/py/arkfunds\n   :alt: PyPI version\n.. image:: https://img.shields.io/github/license/frefrik/arkfunds-python\n   :target: LICENSE\n   :alt: Project Licence\n\n\nA Python library for monitoring `Ark Invest <https://ark-funds.com/>`_ funds data.\n\nInstallation\n------------\n\nInstall the latest release from `PyPI <https://pypi.org/project/arkfunds/>`_\\ :\n\n.. code-block:: console\n\n   pip install arkfunds\n\nQuickstart\n----------\n\n.. code-block:: python\n\n   from arkfunds import ETF, Stock\n\n   # ARK ETFs\n   etf = ETF("ARKK")\n\n   etf.profile()\n   etf.holdings()\n   etf.trades()\n   etf.news()\n\n   # Stocks\n   symbols = ["tsla", "coin", "tdoc"]\n   stock = Stock(symbols)\n\n   stock.profile()\n   stock.fund_ownership()\n   stock.trades()\n\n   stock.price()\n   stock.price_history()\n\nGetting Started\n---------------\nSee our `Getting started guide <https://arkfunds-python.readthedocs.io/en/latest/getting-started.html>`_ in the documentation.\n\nLicense\n-------\n\nThis project is licensed under the **MIT license**. Feel free to edit and distribute this template as you like.\n\nSee `LICENSE <LICENSE>`_ for more information.\n',
    'author': 'Fredrik Haarstad',
    'author_email': 'codemonkey@zomg.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/frefrik/arkfunds-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
