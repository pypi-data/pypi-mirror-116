# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sdgs_tools',
 'sdgs_tools.aplikasi_sdgs',
 'sdgs_tools.aplikasi_sdgs.export',
 'sdgs_tools.aplikasi_sdgs.individu',
 'sdgs_tools.aplikasi_sdgs.keluarga',
 'sdgs_tools.cli',
 'sdgs_tools.ext']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'click>=8.0.1,<9.0.0',
 'openpyxl>=3.0.7,<4.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'uiautomator2>=2.16.7,<3.0.0']

entry_points = \
{'console_scripts': ['sdgs-tools = sdgs_tools.__main__:main']}

setup_kwargs = {
    'name': 'sdgs-tools',
    'version': '0.4.0',
    'description': '',
    'long_description': '# sdgs-tools\n\n[![sdgs-tools - PyPi](https://img.shields.io/pypi/v/sdgs-tools)](https://pypi.org/project/sdgs-tools/)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/sdgs-tools)](https://pypi.org/project/sdgs-tools/)\n[![Donate Saweria](https://img.shields.io/badge/Donasi-Saweria-blue)](https://saweria.co/hexatester)\n[![LISENSI](https://img.shields.io/github/license/hexatester/sdgs-tools)](https://github.com/hexatester/sdgs-tools/blob/main/LICENSE)\n\nAlat bantu sdgs-desa kemendesa.\n\n## Legal / Hukum\n\nKode ini sama sekali tidak berafiliasi dengan, diizinkan, dipelihara, disponsori atau didukung oleh [Kemendesa](https://kemendesa.go.id/) atau afiliasi atau anak organisasinya. Ini adalah perangkat lunak yang independen dan tidak resmi. _Gunakan dengan risiko Anda sendiri._\n',
    'author': 'hexatester',
    'author_email': 'hexatester@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hexatester/sdgs-dashboard',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.10,<4.0.0',
}


setup(**setup_kwargs)
