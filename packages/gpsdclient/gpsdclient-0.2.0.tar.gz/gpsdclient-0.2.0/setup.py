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
    'version': '0.2.0',
    'description': 'A simple gpsd client.',
    'long_description': '# gpsdclient\n\n> A small and simple gpsd client for python 3.\n\nThis package is in active development and not yet published to PyPI.\n\n## Installation\n\nNeeds python 3 installed.\n\nIf you want to use the library, use pip:\n\n```\npip3 install gpsdclient\n```\n\nIf you want to use only the standalone gpsd viewer, I recommend to use pipx:\n\n```\npipx install gpsdclient\n```\n\n## Usage in your scripts\n\n```python\nfrom gpsdclient import GPSDClient\n\nclient = GPSDClient(host="127.0.0.1")\n\n# get your data as json strings:\nfor result in client.json_stream():\n    print(result)\n\n# or as python dicts (optionally convert time information to `datetime.datetime` objects\nfor result in client.dict_stream(convert_datetime=True):\n    print(result)\n```\n\n## Command line usage\n\nYou can use the `gpsdclient` standalone program or execute the module with\n`python3 -m gpsdclient`.\n\n```\n$ gpsdclient --host=192.168.177.151\nConnected to gpsd v3.17\nDevices: /dev/ttyO4\n\nMode  Time                  Lat           Lon           Speed   Track   Alt\n1     n/a                   n/a           n/a           n/a     n/a     n/a\n1     n/a                   n/a           n/a           n/a     n/a     n/a\n1     n/a                   n/a           n/a           n/a     n/a     n/a\n3     n/a                   51.8131231    6.550163817   n/a     n/a     36.025\n3     n/a                   51.8131231    6.550163817   n/a     n/a     36.025\n3     2021-08-13 10:43:38   51.8131231    6.550163817   3.071   304.15  36.025\n3     2021-08-13 10:43:39   51.813239583  6.550226333   2.665   304.03  36.121\n3     2021-08-13 10:43:40   51.813245783  6.550247733   2.418   301.46  36.13\n3     2021-08-13 10:43:41   51.813258883  6.550261517   2.13    306.71  36.257\n3     2021-08-13 10:43:42   51.81326005   6.55025735    2.413   308.88  36.348\n3     2021-08-13 10:43:43   51.813263767  6.550261533   2.557   315.39  36.345\n^C\n```\n\nOr use the raw json mode:\n\n```json\n$ gpsdclient --json\n{"class":"VERSION","release":"3.17","rev":"3.17","proto_major":3,"proto_minor":12}\n{"class":"DEVICES","devices":[{"class":"DEVICE","path":"/dev/ttyO4","driver":"NMEA0183","activated":"2021-08-13T12:25:00.896Z","flags":1,"native":0,"bps":9600,"parity":"N","stopbits":1,"cycle":1.00}]}\n{"class":"WATCH","enable":true,"json":true,"nmea":false,"raw":0,"scaled":false,"timing":false,"split24":false,"pps":false}\n{"class":"SKY","device":"/dev/ttyO4","xdop":0.87,"ydop":1.86,"vdop":0.93,"tdop":2.26,"hdop":1.36,"gdop":3.96,"pdop":1.65,"satellites":[{"PRN":1,"el":84,"az":318,"ss":22,"used":true},{"PRN":22,"el":78,"az":234,"ss":16,"used":true},{"PRN":21,"el":72,"az":115,"ss":0,"used":false},{"PRN":3,"el":55,"az":239,"ss":19,"used":true},{"PRN":17,"el":34,"az":309,"ss":20,"used":true},{"PRN":32,"el":32,"az":53,"ss":32,"used":true},{"PRN":8,"el":21,"az":172,"ss":13,"used":false},{"PRN":14,"el":18,"az":274,"ss":13,"used":false},{"PRN":131,"el":10,"az":115,"ss":0,"used":false},{"PRN":19,"el":9,"az":321,"ss":33,"used":true},{"PRN":4,"el":4,"az":187,"ss":0,"used":false},{"PRN":31,"el":1,"az":106,"ss":0,"used":false},{"PRN":69,"el":80,"az":115,"ss":17,"used":true},{"PRN":84,"el":73,"az":123,"ss":0,"used":false},{"PRN":85,"el":42,"az":318,"ss":26,"used":true},{"PRN":68,"el":33,"az":39,"ss":0,"used":false},{"PRN":70,"el":27,"az":208,"ss":0,"used":false},{"PRN":76,"el":12,"az":330,"ss":19,"used":true},{"PRN":83,"el":12,"az":133,"ss":16,"used":false},{"PRN":77,"el":9,"az":18,"ss":0,"used":false}]}\n{"class":"TPV","device":"/dev/ttyO4","mode":3,"time":"2021-08-13T12:25:01.000Z","ept":0.005,"lat":51.813525983,"lon":6.550081367,"alt":63.037,"epx":13.150,"epy":27.967,"epv":21.390,"track":211.3400,"speed":0.000,"climb":0.000,"eps":62.58,"epc":42.78}\n^C\n```\n\n## Why\n\nI made this because I just needed a simple client library to read the json data gpsd is\nsending.\nThe other python clients have various problems, like 100 % cpu usage, missing python 3\nsupport, license problems or they aren\'t available on PyPI. I also wanted a simple gpsd\nclient to check if everything is working.\n\nThis client is as simple as possible with one exception: It supports the automatic\nconversion of "time" data into `datetime.datetime` objects.\n\nHave fun, hope you like it.\n',
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
