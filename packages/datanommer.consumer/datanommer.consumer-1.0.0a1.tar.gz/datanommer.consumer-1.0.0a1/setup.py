# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datanommer', 'datanommer.consumer']

package_data = \
{'': ['*']}

install_requires = \
['datanommer.models==1.0.0-alpha.1', 'fedora-messaging>=2.1.0,<3.0.0']

entry_points = \
{'moksha.consumer': ['noms = datanommer.consumer:Nommer']}

setup_kwargs = {
    'name': 'datanommer.consumer',
    'version': '1.0.0a1',
    'description': 'Consumer for datanommer',
    'long_description': 'datanommer.consumer\n===================\n\nThis package contains the fedmsg-hub consumer plugin for datanommer.\n\nDatanommer is a storage consumer for the Fedora Infrastructure Message Bus\n(fedmsg).  It is comprised of a `fedmsg <http://fedmsg.com>`_ consumer that\nstuffs every message into a sqlalchemy database.\n',
    'author': 'Fedora Infrastructure',
    'author_email': 'admin@fedoraproject.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fedora-infra/datanommer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
