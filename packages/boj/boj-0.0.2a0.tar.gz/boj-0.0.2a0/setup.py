# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['boj']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'boj',
    'version': '0.0.2a0',
    'description': 'BOJ Offline Judge',
    'long_description': '<!-- Badges -->\n\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/9c0158b110a54cce953d319d5f5b438d)](https://www.codacy.com/gh/Hepheir/BOJ-Offline-Judge/dashboard?utm_source=github.com&utm_medium=referral&utm_content=Hepheir/BOJ-Offline-Judge&utm_campaign=Badge_Grade)\n[![Shields Badge - PyPI/version](https://img.shields.io/pypi/v/boj)](https://pypi.org/project/boj/)\n[![Shields Badge - PyPI/license](https://img.shields.io/pypi/l/boj)](https://pypi.org/project/boj/)\n[![Shields Badge - PyPI/downloads](https://img.shields.io/pypi/dm/boj)](https://pypi.org/project/boj/)\n[![Shields Badge - PyPI/status](https://img.shields.io/pypi/status/boj)](https://pypi.org/project/boj/)\n[![GitHub/issues](https://img.shields.io/github/issues/Hepheir/BOJ-Offline-Judge.svg)](https://github.com/Hepheir/BOJ-Offline-Judge/issues)\n\n# BOJ Offline Judge\n\n## 개요\n\nBOJ-Offline-Judge는 백준 온라인 저지를 CLI, 혹은 Python 스크립트를 통해 이용 하기 위해 제작한 API 입니다.\n\nBOJ는 간단한 JSON혹은 Python의 딕셔너리 형태의 문제 데이터를 제공합니다.\n\n## `BOJProblem`\n\n`boj.BOJProblem()` 객체를 이용하여 문제 데이터에 접근할 수 있습니다.\n\n### 인스턴스 생성\n\n객체의 인스턴스는 다음과 같이 생성합니다.\n\n```python\n>>> from boj import BOJProblem\n>>> problem = BOJProblem(1000)\n```\n\nArgs:\n\n-   `number`: (int) 필수; 문제의 번호입니다.\n\n### 프로퍼티\n\n현재 사용할 수 있는 프로퍼티에는 다음의 값들이 있습니다.\n\n-   `problem_id`: (int) 문제의 번호\n-   `problem_lang`: (int) 문제의 언어 (0: 한국어, 1: 영어)\n-   `title`: (str) 문제의 제목\n-   `description`: (str) 문제의 내용 (HTML 문서)\n-   `input`: (str) 문제의 입력 설명 (HTML 문서)\n-   `output`: (str) 문제의 출력 설명 (HTML 문서)\n-   `hint`: (str) 문제의 힌트 (HTML 문서)\n\n### 예시 코드\n\n다음은 `boj` 모듈을 사용하여 1000번 A+B 문제 데이터를 불러오는 예시 코드 입니다.\n\n```python\n>>> from boj import BOJProblem\n\n>>> problem = BOJProblem(1000)\n\n>>> print(problem.problem_id)\n1000\n\n>>> print(problem.title)\n\'A+B\'\n\n>>> print(problem.data)\n[{\'problem_id\': \'1000\', \'problem_lang\': \'0\', \'title\': \'A+B\', \'description\': \'<p>두 정수 A와 B를 입력받은 다음, ...\', ... }, ... ]\n\n>>> print(problem.json)\nb\'[{"problem_id": "1000", "problem_lang": "0", "title": "A+B", "description": "<p>\\\\ub450 \\\\uc815\\\\uc218 ...\'\n```\n',
    'author': 'Hepheir',
    'author_email': 'hepheir@gmail.com',
    'maintainer': 'Hepheir',
    'maintainer_email': 'hepheir@gmail.com',
    'url': 'https://github.com/Hepheir/BOJ-Offline-Judge',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
