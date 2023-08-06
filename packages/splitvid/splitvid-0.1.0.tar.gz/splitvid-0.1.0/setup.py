# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splitvid']

package_data = \
{'': ['*']}

install_requires = \
['plumbum>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'splitvid',
    'version': '0.1.0',
    'description': 'Split videos with ffmpeg for a certain period',
    'long_description': '# splitvid\n\n![splitvid.png](https://raw.githubusercontent.com/4thel00z/logos/master/splitvid.png)\n\n## Motivation\n\nI need a tool which can split my vids easily, so I can upload them to my story or whatever.\n\n## Installation\n\n```\npip install splitvid\n```\n\n## License\n\nThis project is licensed under the GPL-3 license.\n',
    'author': '4thel00z',
    'author_email': '4thel00z@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/4thel00z/splitvid',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
