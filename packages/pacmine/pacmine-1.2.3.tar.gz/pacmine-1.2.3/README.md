# Pacmine
[![python](https://img.shields.io/pypi/pyversions/minecraft-mod-manager.svg)](https://pypi.org/project/pacmine/1.2.2/)
[![Latest PyPI version](https://img.shields.io/pypi/v/minecraft-mod-manager.svg)](https://pypi.org/project/pacmine/1.2.2/)

![](https://i.imgur.com/ciTThKT.png)

Pacmine makes use of various icons/glyphs from the [NerdFonts](https://www.nerdfonts.com/) collection, so any patched fonts are highly recommended. I personally use Fira Code, but you've got options. Full-color terminals are also recommended -- Windows users can use the [new terminal](https://github.com/microsoft/terminal).  

## Installation
### [pipx](https://github.com/pypa/pipx) (Recommended)
`pipx install pacmine`

### Python
`python -m pip install --user pacmine`

Make sure to add pacmine to your path if user/pipx scripts aren't already.

## Usage
Each command should be prefaced with `pacmine`. Arguments are shown as `{argument_name}`. Arguments with ellipses like `{mods...}` indicate a variable (≥ 1) number of arguments. 

| Command | Description |
| ------ | ------ |
| `add {slugs...}` | Adds 1 or more mods to the local repository, specified by their slugs. Mods cannot be installed multiple times. If you don't know the slug(s), use `search` first.  |
| `remove {slugs...}` | Removes 1 or more mods from the local repository, specified by their slugs. Mods cannot be removed multiple times, nor removed if they are not installed. If you don't know the slug(s), use `list` first. |
| `update` | Checks for and installs any updates to currently installed mods.  | 
| `search {search_term}` | Searches remote repositories and lists any matches to `{search_term}`. | 
| `list` | Lists locally installed mods. |
| `dump` | Dumps a string of slugs for all locally installed mods. Useful with `add` for migrating your mods to another location. | 
| `new {version} {modloader}` | Creates a repository in the current directory for version `{version}` using the `{modloader}` mod loader. It does this with a file called `mods.pkl`, which you shouldn't rename or delete. | 
| `info` | Prints information about pacmine and the local repository, if it exists. | 

Try to avoid deleting files manually from directories managed by pacmine, if possible — pacmine doesn't watch directories to see changes, so it'll become out of sync. 
