# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['struct_tools']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

setup_kwargs = {
    'name': 'struct-tools',
    'version': '0.2.7',
    'description': 'Tools for working with dicts (and lists)',
    'long_description': '# struct-tools\n\nTools for working with data containers/structures,\ni.e. lists, dicts, classes.\n\n- Attribute-access and align-printed dicts.\n- Print functionality also provided as class to be subclassed.\n- Deep (nested) attribute access.\n- Transposing dict-of-dicts, list-of-lists, and mixed.\n- Dict intersection, complement.\n- Cartesian product.\n\n### TODO\n\n- Put DotDict and AlignedDict each in their own module\n\nSee alternatives:\n- <https://github.com/mewwts/addict>\n- <https://github.com/ducdetronquito/scalpl>\n- <https://github.com/srevenant/dictlib>\n- <https://pypi.org/project/dict/>\n- <https://pypi.org/project/dicty/>\n- <https://pypi.org/project/print-dict/>\n- <https://pypi.org/project/dictionaries/>\n- <https://github.com/wolever/pprintpp>\n\nAnswer SO.com questions:\n<https://www.google.com/search?q=python+aligned+dict&oq=python+aligned+dict>\n',
    'author': 'patricknraanes',
    'author_email': 'patrick.n.raanes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
