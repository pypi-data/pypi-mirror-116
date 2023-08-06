# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['requests_cache',
 'requests_cache.backends',
 'requests_cache.models',
 'requests_cache.serializers']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.2,<22.0',
 'cattrs>=1.8,<2.0',
 'itsdangerous>=2.0,<3.0',
 'requests>=2.22,<3.0',
 'url-normalize>=1.4,<2.0',
 'urllib3>=1.25.4,<2.0.0']

extras_require = \
{'all': ['ujson>=4.0',
         'boto3>=1.15,<2.0',
         'botocore>=1.18,<2.0',
         'pymongo>=3.0,<4.0',
         'redis>=3.0,<4.0'],
 'bson': ['bson>=0.5'],
 'docs': ['furo>=2021.8.11-beta.42',
          'myst-parser>=0.15.1,<0.16.0',
          'Sphinx==4.1.2',
          'sphinx-autodoc-typehints>=1.11,<2.0',
          'sphinx-copybutton>=0.3,<0.5',
          'sphinxcontrib-apidoc>=0.3,<0.4',
          'linkify-it-py>=1.0.1,<2.0.0'],
 'docs:python_version >= "3.8"': ['sphinx-inline-tabs>=2021.4.11-beta.9,<2022.0.0'],
 'dynamodb': ['boto3>=1.15,<2.0', 'botocore>=1.18,<2.0'],
 'json': ['ujson>=4.0'],
 'mongodb': ['pymongo>=3.0,<4.0'],
 'redis': ['redis>=3.0,<4.0']}

setup_kwargs = {
    'name': 'requests-cache',
    'version': '0.8.0dev0',
    'description': 'A transparent, persistent cache for the requests library',
    'long_description': "# Requests-Cache\n[![Build](https://github.com/reclosedev/requests-cache/actions/workflows/build.yml/badge.svg)](https://github.com/reclosedev/requests-cache/actions/workflows/build.yml)\n[![Coverage](https://coveralls.io/repos/github/reclosedev/requests-cache/badge.svg?branch=master)](https://coveralls.io/github/reclosedev/requests-cache?branch=master)\n[![Documentation](https://img.shields.io/readthedocs/requests-cache/stable)](https://requests-cache.readthedocs.io/en/stable/)\n[![PyPI](https://img.shields.io/pypi/v/requests-cache?color=blue)](https://pypi.org/project/requests-cache)\n[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/requests-cache)](https://pypi.org/project/requests-cache)\n[![PyPI - Format](https://img.shields.io/pypi/format/requests-cache?color=blue)](https://pypi.org/project/requests-cache)\n[![Code Shelter](https://www.codeshelter.co/static/badges/badge-flat.svg)](https://www.codeshelter.co/)\n\n## Summary\n**requests-cache** is a transparent, persistent cache for the python [requests](http://python-requests.org)\nlibrary. It's a convenient tool to use with web scraping, consuming REST APIs, slow or rate-limited\nsites, or any other scenario in which you're making lots of requests that are expensive and/or\nlikely to be sent more than once.\n\nComplete project documentation can be found at [requests-cache.readthedocs.io](https://requests-cache.readthedocs.io).\n\n## Features\n* **Ease of use:** Use as a [drop-in replacement](https://requests-cache.readthedocs.io/en/stable/api.html#sessions)\n  for `requests.Session`, or [install globally](https://requests-cache.readthedocs.io/en/stable/user_guide.html#patching)\n  to add caching to all `requests` functions\n* **Customization:** Works out of the box with zero config, but with plenty of options available for\n  customizing [cache behavior](https://requests-cache.readthedocs.io/en/stable/user_guide.html#cache-options)\n* **Persistence:** Includes several [storage backends](https://requests-cache.readthedocs.io/en/stable/user_guide.html#cache-backends):\n  SQLite, Redis, MongoDB, GridFS, DynamoDB. Also includes a file-based backend and multiple\n  [serializers](https://requests-cache.readthedocs.io/en/stable/user_guide.html#serializers), so you\n  can store responses as plain JSON files, YAML, and more.\n* **Expiration:** Use [cache headers](https://requests-cache.readthedocs.io/en/stable/user_guide.html#cache-headers),\n  aggressively cache everything for long-term use, use [URL patterns](https://requests-cache.readthedocs.io/en/stable/user_guide.html#url-patterns) for selective caching, or anything in between.\n* **Compatibility:** Can be combined with\n  [other popular libraries based on requests](https://requests-cache.readthedocs.io/en/stable/advanced_usage.html#library-compatibility)\n\n# Quickstart\nFirst, install with pip:\n```bash\npip install requests-cache\n```\n\nThen, use [requests_cache.CachedSession](https://requests-cache.readthedocs.io/en/stable/api.html#sessions)\nto make your requests. It behaves like a normal\n[requests.Session](https://docs.python-requests.org/en/master/user/advanced/#session-objects),\nbut with caching behavior.\n\nTo illustrate, we'll call an endpoint that adds a delay of 1 second, simulating a slow or\nrate-limited website.\n\n**This takes ~1 minute:**\n```python\nimport requests\n\nsession = requests.Session()\nfor i in range(60):\n    session.get('http://httpbin.org/delay/1')\n```\n\n**This takes ~1 second:**\n```python\nimport requests_cache\n\nsession = requests_cache.CachedSession('demo_cache')\nfor i in range(60):\n    session.get('http://httpbin.org/delay/1')\n```\n\nWith caching, the response will be fetched once, saved to `demo_cache.sqlite`, and subsequent\nrequests will return the cached response near-instantly.\n\nIf you don't want to manage a session object, or just want to quickly test it out in your application\nwithout modifying any code, requests-cache can also be installed globally:\n```python\nrequests_cache.install_cache('demo_cache')\nrequests.get('http://httpbin.org/delay/1')\n```\n\n## Next Steps\nTo find out more about what you can do with requests-cache, see:\n\n* The\n  [User Guide](https://requests-cache.readthedocs.io/en/stable/user_guide.html) and\n  [Advanced Usage](https://requests-cache.readthedocs.io/en/stable/advanced_usage.html) sections\n* A working example at Real Python:\n  [Caching External API Requests](https://realpython.com/blog/python/caching-external-api-requests)\n* More examples in the\n  [examples/](https://github.com/reclosedev/requests-cache/tree/master/examples) folder\n",
    'author': 'Roman Haritonov',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/reclosedev/requests-cache',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
