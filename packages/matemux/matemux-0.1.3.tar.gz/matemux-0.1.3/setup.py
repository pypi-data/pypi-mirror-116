# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['matemux']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0']

entry_points = \
{'console_scripts': ['matemux = matemux.__main__:main']}

setup_kwargs = {
    'name': 'matemux',
    'version': '0.1.3',
    'description': 'tmux session generator',
    'long_description': '# matemux\n---\nmatemux is a simple tmux session generator: it generates a session with customized window and pane layouts from a yaml file, called a recipe.\n\n## usage \n\n`$ matemux [RECIPE-FILE-NAME] [--args] [ARGS]...`\n\ncreate the session based on .matemux/RECIPE-FILE-NAME.yml with ARGS following --args flag. `$MATEMUX_DIR` is ~/.matemux by default. You could change it by setting `$MATEMU_DIR` in your environment.\n\n### examples\n`$ matemux example --args --command runserver --port 8000`\ncreate a session based on ~/.matemux/example.yml and pass command=runserver and port=8000 to example.yml commands.\n\n## recipes\neach session is generated from a .yml file called a recipe. a sample recipe is shown below:\n\n`~/.matemux/example.yml`\n\n```\n---\nsession: example\nroot: ~/projects/example\ndefaults:\n  command: runserver\n  port: 8000\ncommands:\n  - source activate venv/bin/activate\n  - C-l\nfocus: sql\nwindows:\n  - window: main\n    focus: 2\n    panes:\n        - pane: 0\n          commands:\n            - htop\n        - pane: 1\n          commands:\n            - neofetch\n          next-split-vertical: true\n        - pane: 2\n          root: ~/projects/example/server\n          commands:\n            - "{{command}} {{port}}"\n  - window: home\n    root: ~/\n```\n\nAt the top level of a .yml file, the following keys could be defined:\n  - `session` is the name of the session to be created. It accepts strings and integer values.\n  - `root` defines the default directory for all virtual terminals in the session. It must be a valid path. By default, it\'s set to \'~/\'.\n  - `defaults` is the default arguments to be passed to commands, we\'ll cover them later on. they should be an object of key-value pairs. It could be omitted.\n  - `commands` are a list of commands that are executed in all virtual terminals in the session. it could be omitted.\n  - `focus` defines the window to focus on at the initial state of the session. By default, it\'s the first window. It accepts strings (name of the window) or integers (window number (0, 1, ...))\n  - `windows` is a list of window configuration, with the following keys:\n    - `window` is the name of the window. It could be omitted, in that case,\n\t  it\'s set by default to its index.\n    - `root` defines the default directory for all panes in the window. It must be\n       a valid path. By default, it\'s set to the session\'s root.\n    - `focus` defines the pane to focus on at the initial state of the window.\n\t  By default, it\'s the first pane (index 0)\n     - `panes` is a list of pane configuration, with the following keys:\n       - `pane` it\'s completely optional and has no effect. It could be set to the pane index to make the .yml file more readable, especially in regards to window focus.\n       - `root` defines the default directory for the pane. It must be a valid path. By default, it\'s set to the parent window\'s root.\n\t   - `commands` are a list of commands to be executed in the pane.\n       - `next-split-vertical` is a boolean that defines whether or not the split for the next pane should be vertical. By default, it\'s set to `false`. Imagine the current layout is like this:\n        ```\n\t\t ----------------\n\t\t |              |\n\t\t |      0       |\n\t\t |              |\n\t\t |              |\n\t\t ----------------\n\t\t ```\n\t\t if it\'s false, when if we define another pane, the new layout would be:\n\t\t ```\n\t\t ----------------\n\t\t |       |      |\n\t\t |   0   |   1  |\n\t\t |       |      |\n\t\t |       |      |\n\t\t ----------------\n\t\t ```\n\t\t but if it\'s true, the new layout would be:\n\t\t ```\n\t\t ----------------\n\t\t |      0       |\n\t\t |______________|\n\t\t |      1       |\n\t\t |              |\n\t\t ----------------\n\t\t ```\n\t\t \nrunning `$ matemux example` creates a session with two windows:\nfirst window is called `main` and has the following layout:\n```\n---------------\n|      |   1  |\n|  0   |______|\n|      |   2  |\n|      |      |\n---------------\n```\n`htop` is running in pane 0, `neofetch` is running in pane 1, and `runserver 8000` is running in in pane 2.\nsecond window is called `home` and has a single pane.\n\n### Notes about commands and defaults:\n  - commands are propagated: If you set some commands for a session, some commands for a window, and some commands for a pane, they\'re all executed in the pane\'s virtual terminal, in that order.\n\n  - You could use custom arguments in commands, in the form `{{arg}}` and pass the arguments through commandline.  For example, if you have a command\n   `mysql -u {{user}}`\n   you could pass user like this:\n    `$ matemux example --args --user myuser`\n  if you want a default value for user, you should set it in session\'s defaults like:\n```\n    defaults:\n      user: myuser\n```\n  - It\'s important to note argument names should only contain characters from the English alphabet and they\'re case-sensitive.\n\n## Author\n[Kamyab Taghizadeh](https://github.com/kamyab.zad)\n',
    'author': 'Kamyab Taghizadeh',
    'author_email': 'kamyab.zad@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kamyabzad/matemux',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
