# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['optic_django_middleware']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2.4,<4.0.0',
 'kubi-ecs-logger>=0.1.0,<0.2.0',
 'optic-sdk>=0.1.0,<0.2.0']

extras_require = \
{'test': ['freezegun>=1.1.0,<2.0.0']}

setup_kwargs = {
    'name': 'optic-django-middleware',
    'version': '0.1.1',
    'description': 'Django Middleware for optic',
    'long_description': '# Optic Django Middleware\n\n<!-- Badges -->\n[![Build status](https://github.com/silentninja/optic-python/actions/workflows/run_tests.yml/badge.svg)](https://github.com/silentninja/optic-python/actions/workflows/run_tests.yml)\n\nThis module is an [Django](https://djangoproject.com/) middleware using [optic-sdk]() to capture and format HTTP data to send to [Optic](https://www.useoptic.com). We have a [list of middleware available for some frameworks](https://github.com/silentninja/optic-python), if we are missing the framework [join our community](https://useoptic.com/docs/community/) and suggest the next framework or develop it with us.\n\n## Requirements\n\nThe module requires `@useoptic/cli` to be installed, instructions on installing it are available [https://www.useoptic.com/docs/](https://www.useoptic.com/docs/).\n\n## Install\n\n```sh\npip install optic-django-middlewaree\n```\n\n## Usage\n\nThe middleware takes a configuration object and captures traffic in the background as long as `@useoptic/cli` is installed.\n\n### Configuration\nEnvironment variables can also be used to set the values\n- `ENABLE`: `boolean` (defaults to `FALSE`) Programmatically control if capturing data and sending it to Optic\n- `UPLOAD_URL`: `string` (defaults to `os.environ[\'OPTIC_LOGGING_URL\']`) The URL to Optics capture URL, if left blank it will expect `OPTIC_LOGGING_URL` environment variable set by the Optic CLI\n- `CONSOLE`: `boolean` (defaults to `FALSE`) Send to stdout/console for debugging\n- `framework`: `string` (defaults to \'\') Additional information to inform Optic of where it is capturing information\n- `LOG`: `boolean` (defaults to `FALSE`) Send to log file\n- `LOG_PATH`: `boolean` (defaults to `./optic.log`) Log file path\n- `LOCAL`: `boolean` (defaults to `TRUE`) Send to optic cli\n- `INTERACTION_MANAGER`: `string` (defaults to `optic_django_middleware.manager.BasicOpticManager`) Manager module to control the behaviour of capturing and sending interaction\n\n### Example\n\n```python\n# settings.py\nimport os\nfrom tempfile import mkdtemp\ntempdir = mkdtemp(\'optic_django\')\nOPTIC = {\n    \'ENABLE\': True,\n    \'LOG_PATH\': os.path.join(tempdir, \'optic.log\'),\n    \'LOG\': True,\n    \'CONSOLE\': False,\n    \'LOCAL\': False\n}\n\nINSTALLED_APPS += [\n    \'optic_django_middleware\',\n]\n\n```\n\nTo start capturing data from the SDK, run your application with\n\n```sh\napi exec "python manage.py runserver"\n```\n\n## License\nThis software is licensed under the [MIT license](../../../LICENSE).\n',
    'author': 'Mukesh',
    'author_email': 'mmukesh95@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/silentninja/optic-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
