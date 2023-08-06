import os

import fire
from semantic_version import Version

from pacmine.core.exceptions import ModNotFoundException, VersionNotFoundException
from pacmine.core.loaders import Loaders
from pacmine.local import log
from pacmine.local.serialize.serializer import Serializer
from pacmine.remote.gateway import Gateway

LOCATION = os.getcwd()
VERSION = "1.2.2"


def add(*slugs: str) -> None:
    """
    Adds one or more mods to the local repository by their slug
    """
    repo = Serializer(LOCATION)
    gateway = Gateway()

    if not repo.is_valid():
        log.error("Not a valid mod repository")
        return

    for slug in slugs:
        if repo.is_installed(slug):
            log.info(f"{slug} is already installed")
            continue

        try:
            result = gateway.download(slug, *repo.get_metadata())
            repo.add(result)
            log.success(f"Installed {slug}")
        except ModNotFoundException:
            log.error(f"{slug} could not be found")
        except VersionNotFoundException:
            log.error(f"No suitable version found for {slug}")


def remove(*slugs: str) -> None:
    """
    Removes one or more mods from the local repository by their slug
    """
    repo = Serializer(LOCATION)

    if not repo.is_valid():
        log.error("Not a valid mod repository")
        return

    for slug in slugs:
        try:
            repo.remove(slug)
            log.success(f"Removed {slug}")
        except ModNotFoundException:
            log.info(f"{slug} is not installed")


def search(search_term: str) -> None:
    """
    Searches mod databases (CurseForge, Modrinth)
    """
    gateway = Gateway()

    results = gateway.search(search_term)

    if not results:
        log.error(f'No results found for "{search_term}"')
        return

    log.print_search_results(results)


def update() -> None:
    """
    Updates local mods, if an update is available for them
    """
    gateway = Gateway()

    repo = Serializer(LOCATION)

    if not repo.is_valid():
        log.error("Not a valid mod repository")
        return

    update_count = 0

    for mod in repo.get_installed_mods():
        is_update = gateway.check_update(mod, *repo.get_metadata())

        if is_update:
            repo.remove(mod.slug)

            new_mod = gateway.update(mod, *repo.get_metadata())

            if not new_mod:
                continue

            repo.add(new_mod)

            log.success(
                f"Updated {new_mod.slug}: {mod.get_date()} -> {new_mod.get_date()}"
            )

            update_count += 1

    log.info(f"Updated {update_count} mods")


def list() -> None:
    """
    List local mods
    """
    repo = Serializer(LOCATION)

    if not repo.is_valid():
        log.error("Not a valid mod repository")
        return

    installed_mods = repo.get_installed_mods()

    if not installed_mods:
        log.info("No mods installed")
        return

    log.print_installed_mods(installed_mods)


def dump() -> None:
    """
    Dumps the slugs of the installed mods
    """
    repo = Serializer(LOCATION)

    if not repo.is_valid():
        log.error("Not a valid mod repository")
        return

    installed_slugs = repo.get_installed_slugs()

    log.print_installed_slugs(installed_slugs)


def new(version_str: float, loader_str: str) -> None:
    """
    Creates a new mod repository in the current directory for a specific version/modloader
    """
    repo = Serializer(LOCATION)

    if repo.is_valid():
        log.warning(
            f"Mod repository already exists in {LOCATION}. Delete mods.pkl and try again."
        )
        return

    try:
        version = Version.coerce(str(version_str))
    except ValueError:
        log.error(f"Invalid version: {version_str}")
        return

    loader = Loaders.from_str(loader_str.lower())
    if loader == Loaders.Unknown:
        log.error(f"Unknown modloader: {loader_str}")
        return

    repo.new(version, loader)


def info():
    """
    Prints information about pacmine and the current repository, if it exists
    """
    log.info(f"Pacmine v{VERSION}")

    repo = Serializer(LOCATION)

    if not repo.is_valid():
        log.error("Not a valid mod repository")
        return

    version, loader = repo.get_metadata()
    log.info(f"Minecraft v{version} using {loader.value}")


def main():
    fire.Fire(
        {
            "add": add,
            "remove": remove,
            "update": update,
            "search": search,
            "list": list,
            "dump": dump,
            "new": new,
            "info": info,
        }
    )


if __name__ == "__main__":
    main()
