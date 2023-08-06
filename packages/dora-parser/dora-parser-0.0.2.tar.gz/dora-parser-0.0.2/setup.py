# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dora_parser', 'dora_parser.dialects']

package_data = \
{'': ['*']}

install_requires = \
['mo-sql-parsing>=0.1.2,<0.2.0',
 'pandas>=1.3.0,<2.0.0',
 'seaborn>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'dora-parser',
    'version': '0.0.2',
    'description': 'SQL Parser ans Transpiler',
    'long_description': "# Parser\n\nDora's [parser](https://en.wikipedia.org/wiki/Parsing) and [transpiler](https://en.wikipedia.org/wiki/Source-to-source_compiler) tool for some big data **SQL** dialects, based on [Mozilla SQL Parser](https://github.com/mozilla/moz-sql-parser)  project.\n\n## Getting Started\n\nYou can install the library using pip:\n\n```sh\npip install dora-parser\n```\n\n## Getting Help\n\nWe use GitHub [issues](https://github.com/doraproject/parser/issues) for tracking [bugs](https://github.com/doraproject/parser/labels/bug), [questions](https://github.com/doraproject/parser/labels/question) and [feature requests](https://github.com/doraproject/parser/labels/enhancement).\n\n## Contributing\n\nPlease read through this [contributing](.github/CONTRIBUTING.md) document to get start and before submitting any issues or pull requests to ensure we have all the necessary information to effectively respond to your contribution.\n\n---\n\n[Dora Project](https://github.com/doraproject) is a recent open-source project based on technology developed at [Compasso UOL](https://compassouol.com/)\n",
    'author': 'DataLabs',
    'author_email': 'time.dataanalytics.datalabs@compasso.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/doraproject/parser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
