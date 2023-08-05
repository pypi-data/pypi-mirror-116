# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sentipy', 'sentipy.tests']

package_data = \
{'': ['*']}

install_requires = \
['beartype>=0.7.1,<0.8.0',
 'requests>=2.26.0,<3.0.0',
 'websocket-client>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'sentiment-investor',
    'version': '2.1.0',
    'description': 'Access the Sentiment Investor API through Python',
    'long_description': "# SentiPy\n\n> Welcome to the Sentiment Investor API wrapper. This package can be used to easily access trending stocks and individual ticker data from the sentimentinvestor.com website. \n\n## Installing\n\nSentiPy can be installed with [pip](https://pip.pypa.io/en/stable/):\n\n```\n$ python3 -m pip install sentiment-investor\n```\n\nOn macOS, it can also be installed via [MacPorts](https://ports.macports.org/port/py-sentipy/):\n\n```\n$ sudo port install py-sentipy\n```\n\n## Setup\n\nTo use this package you will need a developer token and key, which can be obtained from [sentimentinvestor.com/developer/dashboard](https://sentimentinvestor.com/developer/dashboard). \n\n## Documentation\n\nSentiPy has usage and reference documentation at [sentimentinvestor.com/developer/python-docs](https://sentimentinvestor.com/developer/python-docs).\n\n## 🤝 Contributing\n\nContributions, issues and feature requests are welcome!<br />Feel free to check the [issues page](https://github.com/sentimentinvestor/sentipy/issues).\n\n### Geting Started\n\nFirst, fork the [GitHub project](https://github.com/sentimentinvestor/sentipy) to your account. Then, run the following with your GitHub handle in place of `INSERT_GITHUB_NAME`:\n\n```sh\n$ git clone https://github.com/INSERT_GITHUB_NAME/sentipy\n$ cd sentipy\n$ poetry install && poetry shell\n$ pre-commit install\n```\n\nThis then runs the formatters when you're about to commit any changes.\n\n### Authors\n\nThe following people have made notable contributions to the development of this library (in chronological order):\n\n- [Rob Stock](https://github.com/lipton-green-tea)\n- [Timothy Langer](https://github.com/ZeevoX)\n- [Haren S](https://github.com/harens)\n\nThe full list of contributors is [here](https://github.com/sentimentinvestor/sentipy/graphs/contributors).\n\n## Licence\n\nSentiPy is made available under the MIT Licence. For more details, see [LICENSE.txt](https://github.com/sentimentinvestor/sentipy/blob/master/LICENSE).\n",
    'author': 'Robert Stok',
    'author_email': 'rs.stok@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://sentimentinvestor.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
