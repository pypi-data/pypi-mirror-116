# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gpsdclient']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['gpsdclient = gpsdclient.cli:main']}

setup_kwargs = {
    'name': 'gpsdclient',
    'version': '0.1.0',
    'description': 'A simple gpsd client.',
    'long_description': '# gpsdclient\n\n> A small and simple gpsd client for python 3.\n\nThis package is in active development and not yet published to PyPI.\n\n## Installation\n\nNeeds python 3 installed.\n\nIf you want to use the library, use pip:\n\n```\npip3 install gpsdclient\n```\n\nIf you want to use only the standalone gpsd viewer, I recommend to use pipx:\n\n```\npipx install gpsdclient\n```\n\n## Usage in your scripts\n\n```python\nfrom gpsdclient import GPSDClient\n\nclient = GPSDClient(host="127.0.0.1")\n\n# get your data as json strings:\nfor result in client.json_stream():\n    print(result)\n\n# or as python dicts (optionally convert time information to `datetime.datetime` objects\nfor result in client.dict_stream(convert_datetime=True):\n    print(result)\n```\n\n## Command line usage\n\nYou can use the `gpsdclient` standalone program or execute the module with\n`python3 -m gpsdclient`.\n\n```\n$ gpsdclient --host=192.168.177.151\nConnected to gpsd v3.17\nDevices: /dev/ttyO4\n\nMode  Time                  Lat           Lon           Speed   Track   Alt\n1     n/a                   n/a           n/a           n/a     n/a     n/a\n1     n/a                   n/a           n/a           n/a     n/a     n/a\n1     n/a                   n/a           n/a           n/a     n/a     n/a\n3     n/a                   51.8131231    6.550163817   n/a     n/a     36.025\n3     n/a                   51.8131231    6.550163817   n/a     n/a     36.025\n3     2021-08-13 10:43:38   51.8131231    6.550163817   3.071   304.15  36.025\n3     2021-08-13 10:43:39   51.813239583  6.550226333   2.665   304.03  36.121\n3     2021-08-13 10:43:40   51.813245783  6.550247733   2.418   301.46  36.13\n3     2021-08-13 10:43:41   51.813258883  6.550261517   2.13    306.71  36.257\n3     2021-08-13 10:43:42   51.81326005   6.55025735    2.413   308.88  36.348\n3     2021-08-13 10:43:43   51.813263767  6.550261533   2.557   315.39  36.345\n^C\n```\n\n## Why\n\nI made this because I just needed a simple client library to read the json data gpsd is\nsending.\nThe other python clients have various problems, like 100 % cpu usage, missing python 3\nsupport, license problems or they aren\'t available on PyPI. I also wanted a simple gpsd\nclient to check if everything is working.\n\nThis client is as simple as possible with one exception: It supports the automatic\nconversion of "time" data into `datetime.datetime` objects.\n\nHave fun, hope you like it.\n',
    'author': 'Thomas Feldmann',
    'author_email': 'mail@tfeldmann.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
