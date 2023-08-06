# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zodipy']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=4.3.1,<5.0.0',
 'astroquery>=0.4.3,<0.5.0',
 'healpy>=1.15.0,<2.0.0',
 'numpy>=1.21.1,<2.0.0',
 'scipy>=1.7.1,<2.0.0']

setup_kwargs = {
    'name': 'zodipy',
    'version': '0.1.0',
    'description': 'Zodipy is a python tool that simulates the instantaneous Zodiacal emission as seen from an observer.',
    'long_description': "# Zodipy\n\n## Description\nZodipy is a python tool that simulates the instantaneous Zodiacal emission as seen from an observer.\n\n## Usage\nThe following will produce a HEALPIX map at `NSIDE=128` of the simulated\nemission as seen by the Planck satellite today\n```python\nimport zodipy\n\nzodi = zodipy.Zodi(observer='Planck')\nemission = zodi.simulate(nside=256, freq=800)\n```\n\nThe time of observation is defined as following\n```python\nimport datetime\n\ntime = datetime(2010, 1, 1)\nzodi = zodipy.Zodi(observer='L2', observation_time=time)\nemission = zodi.simulate(nside=256, freq=800)\n```\n\nThe simulated emission can be visualized using Healpy and matplotlib\n```python\nimport healpy as hp\nimport matplotlib.pyplot as plt\n\nhp.mollview(\n    emission, \n    norm='hist', \n    unit='W/m^2 Hz sr', \n    title='Zodiacal Emission as seen from L2 (2010-01-01)', \n)\nplt.show()\n```\n![plot](imgs/zodi.png)",
    'author': 'Metin San',
    'author_email': 'metinisan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MetinSa/zodipy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
