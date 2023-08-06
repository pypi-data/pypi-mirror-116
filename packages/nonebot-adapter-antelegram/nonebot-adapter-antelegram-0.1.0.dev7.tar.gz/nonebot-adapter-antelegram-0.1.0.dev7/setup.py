# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot', 'nonebot.adapters.telegram']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.18.0,<0.19.0', 'nonebot2>=2.0.0a15,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-adapter-antelegram',
    'version': '0.1.0.dev7',
    'description': 'Another unofficial Telegram adapter for nonebot2',
    'long_description': '<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://raw.githubusercontent.com/nonebot/nonebot2/master/docs/.vuepress/public/logo.png" width="200" height="200" alt="nonebot"></a>\n</p>\n\n<div align="center">\n\n# NoneBot-Adapter-DING\n\n_✨ 钉钉协议适配 ✨_\n\n</div>\n',
    'author': 'ColdThunder11',
    'author_email': 'lslyj27761@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ColdThunder11/nonebot-adapter-telegram',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
