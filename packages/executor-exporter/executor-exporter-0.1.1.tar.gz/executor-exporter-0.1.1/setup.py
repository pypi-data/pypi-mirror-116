# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['executor_exporter']

package_data = \
{'': ['*']}

install_requires = \
['prometheus-client>=0.11.0,<0.12.0']

setup_kwargs = {
    'name': 'executor-exporter',
    'version': '0.1.1',
    'description': '',
    'long_description': '# executor-exporter\n[![codecov](https://codecov.io/gh/ygormutti/executor-exporter/branch/main/graph/badge.svg?token=FIXME)](https://codecov.io/gh/ygormutti/executor-exporter)\n[![CI](https://github.com/ygormutti/executor-exporter/actions/workflows/main.yml/badge.svg)](https://github.com/ygormutti/executor-exporter/actions/workflows/main.yml)\n\nA [Prometheus](https://prometheus.io/) exporter for Python [`concurrent.futures`](https://docs.python.org/3/library/concurrent.futures.html) executors. Provides instrumented drop-in replacements for `ThreadedPoolExecutor` and `ProcessPoolExecutor`.\n\n![water level ruler photo](docs/water_level_ruler.jpg)\n\n*Public domain photo by Patsy Lynch. [More info](https://commons.wikimedia.org/wiki/File:FEMA_-_40847_-_A_water_level_ruler_in_North_Dakota.jpg)*\n\n## Install it from PyPI\n\n```bash\npip install executor-exporter\n```\n\n## Usage\n\n```py\nfrom executor_exporter import ThreadPoolExecutor\n# or\nfrom executor_exporter import ProcessPoolExecutor\n```\n\nIf you stick to the public APIs of `concurrent.future` executors (consisting of `__init__`, `submit` and `map` methods), you just need to replace the builtin executor with its instrumented version provided by this package.\n\nThe provided executors act as [proxies](https://en.wikipedia.org/wiki/Proxy_pattern) for the builtin executor while collecting the following metrics:\n\n<!-- begin metrics_table -->\n<!-- end metrics_table -->\n\n### Additional parameters\n\nThe `__init__` methods of the instrumented executors take two additional optional parameters:\n\n| Parameter     | Type                                  | Default value                                   | Description                                                                                                                                                                                                   |\n| ------------- | ------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |\n| `exporter_id` | `str`                                 | `""`                                            | This id is used as the value for the `exporter` label in all metrics. Useful when your app uses multiple executors and you want to measure them separately                                                    |\n| `registry`    | `prometheus_client.CollectorRegistry` | `prometheus_client.REGISTRY` (default registry) | Useful when you\'re using a registry other than the default for whatever reason, e.g. using `prometheus_client` [multiprocess mode](https://github.com/prometheus/client_python#multiprocess-mode-eg-gunicorn) |\n\n### Custom executors\n\nThe `InstrumentedExecutorProxy` class does the heavy-lifting. If you\'re using a custom executor, you can still instrument them by using wrapping it:\n\n```py\nfrom executor_exporter import InstrumentedExecutorProxy, ExecutorExporter\n\nmax_workers = 42\nexecutor = YourCustomExecutor(max_workers)\nexporter = ExecutorExporter(executor)\n\ninstrumented_executor = InstrumentedExecutorProxy(executor, exporter, max_workers)\n```\n',
    'author': 'Ygor Mutti',
    'author_email': 'ygormutti@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
