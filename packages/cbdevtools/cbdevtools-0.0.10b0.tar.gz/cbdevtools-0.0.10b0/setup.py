# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cbdevtools']

package_data = \
{'': ['*']}

install_requires = \
['orpyste>=1.3.2-beta.0,<2.0.0']

setup_kwargs = {
    'name': 'cbdevtools',
    'version': '0.0.10b0',
    'description': '"Common Box of Dev Tools" proposing small scripts that can be helpful.',
    'long_description': 'The `Python` module `cbdevtools`\n================================\n\n\n> **I beg your pardon for my english...**\n>\n> English is not my native language, so be nice if you notice misunderstandings, misspellings, or grammatical errors in my documents and codes.\n\n\nAbout `cbdevtools`\n-----------------\n\nThis project is a "Common Box of Dev Tools" (the name comes also from "Christophe BAL Dev Tools"). `cbdevtools` proposes small scripts that can be helpful..., at least for the author of this package.\n\n\nWhat can be do and how?\n-----------------------\n\nSee directly each small scripts for more informations.\n\n\n<!-- :tutorial-START: -->\n<!-- :tutorial-END: -->\n\n\n<!-- :version-START: -->\n<!-- :version-END: -->\n',
    'author': 'Christophe BAL',
    'author_email': None,
    'maintainer': 'Christophe BAL',
    'maintainer_email': None,
    'url': 'https://github.com/projetmbc/tools-for-dev/tree/master/cbdevtools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
