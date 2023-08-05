# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['inginious_coding_style']

package_data = \
{'': ['*'], 'inginious_coding_style': ['templates/*']}

install_requires = \
['inginious>=0.7,<0.8', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'inginious-coding-style',
    'version': '1.4.0',
    'description': '',
    'long_description': '# INGInious Coding Style\n\nINGInious Coding Style is a plugin for INGInious 0.7 and up that allows tutors to grade several aspect of student submissions\' coding style.\n\nINGInious Coding Style should be easy to use for both tutors and students. The plugin adds new buttons and elements to various existing menus in the application that can be used to add and view coding style grades.\n\n## Documentation\n\nFull documentation can be found here: https://pederha.github.io/inginious-coding-style/\n\n## Installation\n\n```bash\npip install inginious-coding-style\n```\n\n## Configuration\n\nINGInious Coding Style is highly configurable and provides granular control of the majority of its features. Despite this, extensive configuration is not necessary, as the plugin tries to implement sensible defaults, and therefore should just work straight out of the box.\n\n### Minimal Configuration\n\nThe following YAML snippet provides the default plugin configuration, and is a good starting point for exploring the plugin\'s functionality:\n\n```yml\nplugins:\n-   plugin_module: inginious_coding_style\n    name: "INGInious Coding Style"\n```\n\n### Full Configuration\n\nBelow is an example of a configuration making use of all available configuration options.\n\n```yml\nplugins:\n-   plugin_module: inginious_coding_style\n    name: "INGInious Coding Style"\n    enabled:\n        # This enables all default categories + 1 custom category\n        - comments\n        - modularity\n        - structure\n        - idiomaticity\n        - coolness # Our custom category\n    categories:\n        # This is a definition for a new category\n      - id: coolness\n        name: Coolness\n        description: How cool the code looks B-)\n      # This redefines a default category\n      - id: comments\n        name: Kommentering\n        description: Hvor godt kommentert koden er.\n    submission_query:\n        header: CSG\n        priority: 3000\n        button: true\n    weighted_mean:\n        enabled: true\n        weighting: 0.25\n        round: true\n        round_digits: 2\n    task_list_bars:\n        total_grade:\n            enabled: true\n            label: Grade\n        base_grade:\n            enabled: true\n            label: Correctness\n        style_grade:\n            enabled: true\n            label: Coding Style\n```\n\n<!-- ## Known Issues -->\n\n## TODO\n\n### User Features\n\n- [ ] Make each coding style grade progress bar on `/course/<courseid>` a clickable element that links to the relevant coding style grades page (`/submission/<submissionid>/codingstyle`) for\nthe relevant task.\n\n### Admin/Tutor Features\n\n- [ ] Add `graded_by: List[str]` attribute to `CodingStyleGrades` to record which admin/tutor graded the submission\'s coding style.\n\n### Plugin Configuration\n\n- [ ] Add ability to enable/disable grading categories on a per-course basis.\n- [ ] Add ability to enable/disable plugin on a per course-basis.\n\n### Robustness\n\n- [ ] Better exception handling for Pydantic `ValidationError`. If something fails to validate, we should be able to display human-readable messages both in the web interface and in the logs.\n- Add an "admin/tutor only" decorator that can be applied to methods that bars student users from calling them.\n- [ ] Ability to revert submission grades to their base grades if `weighted_mean` is disabled.\n    - Would need to be a button that when clicked iterates through top submissions (`user_tasks` collection), then for each submission queries the `submissions` collection and fetches the grade stored in the submission with the corresponding `_id` and overwrites the grade in `user_tasks`.\n\n\n<!-- - [x] Complete -->\n<!-- - [ ] Incomplete -->\n\n## Developer Notes\n\nThis plugin uses [htmx](https://htmx.org/) to provide some interactivity.\n',
    'author': 'Peder Hovdan Andresen',
    'author_email': 'pedeha@stud.ntnu.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PederHA/inginious-coding-style',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
