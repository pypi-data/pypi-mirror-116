# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dict2sql',
 'dict2sql.dialects',
 'dict2sql.dialects.ansi',
 'dict2sql.test_fixtures']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.13,<2.0.0',
 'toolz>=0.11.1,<0.12.0',
 'typing-extensions>=3.10.0,<4.0.0']

setup_kwargs = {
    'name': 'dict2sql',
    'version': '2.1.0',
    'description': '',
    'long_description': '# dict2sql, the missing SQL API\n\ndict2sql gives you the ability to express SQL as python data structures.\n\n[![pypi badge](https://badge.fury.io/py/dict2sql.svg)](https://badge.fury.io/py/dict2sql)\n\n# A simple example\n\n```python\nfrom dict2sql.types import SelectStatement\nfrom dict2sql import dict2sql\n\nquery: SelectStatement = {\n    "Select": ["name", "height", "country"],\n    "From": ["mountains"],\n    "Where": {\n        "Op": "AND",\n        "Predicates": [\n            {"Op": ">=", "Sx": "height", "Dx": "3000"},\n            {"Op": "=", "Sx": "has_glacier", "Dx": "true"}\n        ],\n    },\n    "Limit": 3\n}\n\ndict2sql = dict2sql()\n\nprint(dict2sql.to_sql(query))\n\n```\n\nproduces\n\n```sql\nSELECT `name` , `height` , `country`\nFROM `mountains`\nWHERE ( ( height >= 3000 ) AND ( has_glacier = true ) )\nLIMIT 3\n```\n\n\n# Installing\n\n```shell\n$ pip install -U dict2sql\n\n```\n\n\n# Notes\n\n\n## Rationale\n\nFor historical reasons in the world of relational databases interfaces usually consist of domain-specific languages (mostly dialects of SQL)\nrather than composition of data structures as it is common with modern APIs (for example JSON-based REST, protobuf).\nWhile a domain-specific language (DSL) is very well suited for interactive use, such as manually exploring a dataset, this approach has some limitations when trying to interface with a database programmatically (for example from a Python script).\n\nThis library brings a modern API to SQL databases, allowing the user to express queries as composition of basic python data structures: dicts, lists, strings, ints, floats and booleans.\n\nAmong the primary benefits of this approach is a superior ability to reuse code. All the usual python constructs and software engineering best practices are available to the query author to express queries using clean, maintainable code.\n\nQuery-as-data also means compatibility with Python\'s type hinting system, which translates to reduced query-correctness issues, improved error messages (at least with respect to some query engines), and a quicker development experience.\n\nNotably, this solution eliminates one major source of friction with traditional programming-language level handling of SQL: SQL injection and excaping. While solutions to this problem such as parametrized queries have been developed over time, they heavily favor safety at the expense of expressivity; it is usually forbidden to compose parametrized queries at runtime.\nHow is this accomplished? By having granular information about each component of a query, `dict2sql` is easily able to apply escaping where needed, resulting in safe queries.\n\nFinally, it should be noted that this library strictly tries to do *one* job well, namely *composing sql queries*. There is many related functionalities in this space which we explicitely avoid taking on, feeling that they are best left to other very mature libraries in the Python ecosystem. For example: connecting to the database and performing queries, parsing query return values.\n\n- code reuse\n- types\n- small concern, only translating to sql\n- safety\n\n## Implementation details\nThis project at the moment targets ANSI SQL, with the ambition of soon targeting all major SQL dialects.\n\nTests are based on the [Chinhook Database](https://github.com/lerocha/chinook-database).\n\n## Best with\n\nA user of this library would naturally want to obtain the results of queries as data structures as well (a sql2dict of sorts).\nThis functionality already provided by the excellent [records](https://pypi.org/project/records/) library.\n\n## Contributing\n\nContributions and forks are welcome!\n\nIf you want to increment the current language to increase coverage of ANSI SQL, go right ahead.\n\nIf you plan to contribute major features such as support for a new dialect, it is recommended to start a PR early on in the development process to prevent duplicate work and ensure that it will be possible to merge the PR without any hiccups.\n\nIn any case, thank you for your contribution!\n\n\n### TODOs\n- implement sanitization/escaping correctly\n- sql functionality\n    - having\n    - functions\n    - aggregate\n    - statements\n        - create\n- more examples\n    - query end to end with sqlalchemy\n    - generative examples\n- handle different dialects\n    - sqlite\n    - mysql\n    - postgres\n- implement tests\n    - unit tests\n        - compiler to ir\n        - ir to sql\n        - utils\n    - security\n        - test for sql injection\n            - fuzzing\n            - generative testing\n',
    'author': 'Simon Accascina',
    'author_email': 'simon@accascina.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/simonacca/dict2sql',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
