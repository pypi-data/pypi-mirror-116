# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['health_indices']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'health-indices',
    'version': '0.0.1',
    'description': 'a unified collection of health indices and indicators eg bmi,bai,etc',
    'long_description': '# health-indices\nA unified collection of health indices and health indicators eg bmi,bai,corp index,etc\n\n#### Purpose of the Package\n+ The purpose of the package is to provide a collection of all health indices in one unified libary\n\n\n### Features\n+ Collection of Health Indices\n\t- BMI\n\t- BAI\n\t- Corpulence Index\n\t- Piglet Indices\n\t- etc \n+ Collection of Health Indicators\n\t- Mortality rate\n\t- Birth rate\n\t- Prevalence Rate\n\t- Fertility rate\n\n\n\n\n### Getting Started\nThe package can be found on pypi hence you can install it using pip\n\n#### Installation\n```bash\npip install health_indices\n```\n\n\n### Usage\nUsing the short forms or abbreviated forms of indices\n```python\n>>> from health_indices import bmi,bai,\n>>> bmi(54,1.70)\n\n```\n\nUsing the long form of indices\n```python\n>>> from health_indices import bodymassindex\n>>> bodymassindex(54,1.70)\n\n```\n\n#### Examples\n```python\n>>> from health_indices import bmi\n>>> bmi(54,1.70)\nBody Mass Index is =>  18.0\nBMI Category => Underweight \nBody Mass Index is =>  18.0\n18.0\n>>> a = bmi(54,1.70)\nBody Mass Index is =>  18.0\nBMI Category => Underweight \nBody Mass Index is =>  18.0\n>>> a\n18.0\n>>> \n\n```\n\n### Contribution\nContributions are welcome\nNotice a bug let us know. Thanks\n\n\n### Author\n+ Main Maintainer: Jesse E.Agbe(JCharis)\n+ Jesus Saves @JCharisTech\n',
    'author': 'Jesse E.Agbe(JCharis)',
    'author_email': 'jcharistech@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jcharistech/health-indices',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
