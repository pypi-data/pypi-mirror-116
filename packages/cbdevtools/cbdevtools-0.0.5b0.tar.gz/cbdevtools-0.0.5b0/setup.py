# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cbdevtools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cbdevtools',
    'version': '0.0.5b0',
    'description': '???',
    'long_description': 'The `Python` module `cbdevtools`\n================================\n\n\n> **I beg your pardon for my english...**\n>\n> English is not my native language, so be nice if you notice misunderstandings, misspellings, or grammatical errors in my documents and codes.\n\n\nAbout `cbdevtools`\n-----------------\n\nThis project is a "Common Box of Dev Tools". It proposes small scripts taht can be helpful, at least to the author of this package. :-) \n\n\n????\n----\n\n\n\n<!-- :tutorial-START: -->\n<!-- :tutorial-END: -->\n\n\n<!-- :version-START: -->\n<!-- :version-END: -->\n',
    'author': 'Christophe BAL',
    'author_email': None,
    'maintainer': 'Christophe BAL',
    'maintainer_email': None,
    'url': 'https://github.com/projetmbc/tools-for-dev/tree/master/cbdevtools',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
