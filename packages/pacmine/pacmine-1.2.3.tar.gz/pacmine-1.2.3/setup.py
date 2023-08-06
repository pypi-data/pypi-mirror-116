# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pacmine',
 'pacmine.core',
 'pacmine.local',
 'pacmine.local.discovery',
 'pacmine.local.serialize',
 'pacmine.remote']

package_data = \
{'': ['*']}

install_requires = \
['Columnar>=1.3.1,<2.0.0',
 'arrow>=1.1.1,<2.0.0',
 'fire>=0.4.0,<0.5.0',
 'requests>=2.26.0,<3.0.0',
 'semantic-version>=2.8.5,<3.0.0',
 'termcolor>=1.1.0,<2.0.0',
 'tqdm>=4.62.0,<5.0.0']

entry_points = \
{'console_scripts': ['pacmine = pacmine.__main__:main']}

setup_kwargs = {
    'name': 'pacmine',
    'version': '1.2.3',
    'description': 'Simple package manager-esque mod manager for Minecraft',
    'long_description': "# Pacmine\n[![python](https://img.shields.io/pypi/pyversions/minecraft-mod-manager.svg)](https://pypi.org/project/pacmine/1.2.2/)\n[![Latest PyPI version](https://img.shields.io/pypi/v/minecraft-mod-manager.svg)](https://pypi.org/project/pacmine/1.2.2/)\n\n![](https://i.imgur.com/ciTThKT.png)\n\nPacmine makes use of various icons/glyphs from the [NerdFonts](https://www.nerdfonts.com/) collection, so any patched fonts are highly recommended. I personally use Fira Code, but you've got options. Full-color terminals are also recommended -- Windows users can use the [new terminal](https://github.com/microsoft/terminal).  \n\n## Installation\n### [pipx](https://github.com/pypa/pipx) (Recommended)\n`pipx install pacmine`\n\n### Python\n`python -m pip install --user pacmine`\n\nMake sure to add pacmine to your path if user/pipx scripts aren't already.\n\n## Usage\nEach command should be prefaced with `pacmine`. Arguments are shown as `{argument_name}`. Arguments with ellipses like `{mods...}` indicate a variable (≥ 1) number of arguments. \n\n| Command | Description |\n| ------ | ------ |\n| `add {slugs...}` | Adds 1 or more mods to the local repository, specified by their slugs. Mods cannot be installed multiple times. If you don't know the slug(s), use `search` first.  |\n| `remove {slugs...}` | Removes 1 or more mods from the local repository, specified by their slugs. Mods cannot be removed multiple times, nor removed if they are not installed. If you don't know the slug(s), use `list` first. |\n| `update` | Checks for and installs any updates to currently installed mods.  | \n| `search {search_term}` | Searches remote repositories and lists any matches to `{search_term}`. | \n| `list` | Lists locally installed mods. |\n| `dump` | Dumps a string of slugs for all locally installed mods. Useful with `add` for migrating your mods to another location. | \n| `new {version} {modloader}` | Creates a repository in the current directory for version `{version}` using the `{modloader}` mod loader. It does this with a file called `mods.pkl`, which you shouldn't rename or delete. | \n| `info` | Prints information about pacmine and the local repository, if it exists. | \n\nTry to avoid deleting files manually from directories managed by pacmine, if possible — pacmine doesn't watch directories to see changes, so it'll become out of sync. \n",
    'author': 'aidan',
    'author_email': 'aidan.chaplin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/TheBicameralMind/pacmine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
