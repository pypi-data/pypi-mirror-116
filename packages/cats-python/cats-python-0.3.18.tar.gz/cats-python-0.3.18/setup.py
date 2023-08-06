# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cats', 'cats.server']

package_data = \
{'': ['*']}

install_requires = \
['orjson>=3.5.4,<4.0.0',
 'pytz>=2021.1,<2022.0',
 'sentry-sdk>=1.1.0,<2.0.0',
 'tornado>=6.1,<7.0']

extras_require = \
{'django': ['Django>=2.0,<3.0', 'djangorestframework>=3.12.4'],
 'djantic': ['Django>=2.0,<3.0', 'pydantic>=1.8.2', 'djantic>=0.3.3'],
 'pydantic': ['pydantic>=1.8.2']}

setup_kwargs = {
    'name': 'cats-python',
    'version': '0.3.18',
    'description': 'Cifrazia Action Transport System for Python',
    'long_description': '# CATS Python\n\n## Cifrazia Action Transport System\n\n### Requirements\n\n+ Python `^3.9`\n+ Tornado `^6.1`\n+ Sentry SDK `^1.1.0`\n+ uJSON `^4.0.2`\n+ PyTZ `^2021.1`\n\n**Extras**\n\n+ `django`\n  + Django `^2.2` (optional)\n  + Django Rest Framework `^3.12.4` (optional)\n\n### Installation\n\n**Install via Poetry**\n\n```shell\npoetry add cats-python\n```\n\nWith `Django` support:\n\n```shell\npoetry add cats-python[django]\n```\n\n# [WIP] Protocol declaration\n\n## Compression\n\n### Compression algorithms\n\n`0x00` **No compression**\n\nAll payload in not compressed (unless the payload itself is a compressed data)\n\n`0x01` **GZip**\n\nPayload compressed with GZip at level 6\n\n`0x02` **ZLib**\n\nPayload compressed with ZLib DEFLATE method at level 6\n\nAdditional header with **Adler32** checksum provided `{"Adler32": 1235323}` ',
    'author': 'Bogdan Parfenov',
    'author_email': 'adam.brian.bright@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AdamBrianBright/cats-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
