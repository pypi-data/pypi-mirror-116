# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paud']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'paud',
    'version': '0.1',
    'description': 'Python library to process audio',
    'long_description': "# paud\nPython library to process audio\n\n\n\nopen audio\n\n```python\nfrom paud import Audio\n\nau = Audio.open('audio.wav') #file or path\n\nprint(f'audio duration = {au.duration}')\n\nau.play() #play audio\n\nau[:100].play() #play first 100 frames of audio\n\n\n```\n\n\n\nopen audio from URL\n\n```python\nimport requests\nfrom paud import Audio\nfrom io import BytesIO\n\nr = requests.get('https://file-examples-com.github.io/uploads/2017/11/file_example_WAV_10MG.wav')\n\nau = Audio.open(BytesIO(r.content))\nau.play()\n```\n\n",
    'author': 'ASVIEST',
    'author_email': '71895914+ASVIEST@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ASVIEST/paud',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
