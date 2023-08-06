import arrow

from typing import List, Optional
from semantic_version import Version

from . import api
from .api import Sites
from .curse_api import CurseAPI
from .dl_result import DownloadResult
from .modrinth_api import ModrinthAPI
from ..core.exceptions import ModNotFoundException, VersionNotFoundException
from ..core.loaders import Loaders
from ..core.search_result import SearchResult


class Gateway:
    def __init__(self):
        self.curse_api = CurseAPI(api.curse_base)
        self.modrinth_api = ModrinthAPI(api.modrinth_base)

    def search(self, search_term) -> List[SearchResult]:
        curse_results = self.curse_api.search(search_term)
        modrinth_results = self.modrinth_api.search(search_term)

        return sorted((*curse_results, *modrinth_results), key=lambda x: x.name)

    def download(self, slug: str, version: Version, loader: Loaders) -> DownloadResult:
        try:
            return self.curse_api.download(slug, version, loader)
        except (ModNotFoundException, VersionNotFoundException):
            return self.modrinth_api.download(slug, version, loader)

    def check_update(
        self, downloaded_mod: DownloadResult, version: Version, loader: Loaders
    ) -> bool:
        date_updated = downloaded_mod.date_updated
        mod_id = downloaded_mod.mod_id
        site = downloaded_mod.source

        if site == Sites.Curseforge:
            latest_download = self.curse_api.get_latest_download(
                mod_id, version, loader
            )
            latest_download_date = arrow.get(latest_download["fileDate"])

            return latest_download_date > date_updated

        elif site == Sites.Modrinth:
            latest_download = self.modrinth_api.get_latest_download(
                mod_id, version, loader
            )
            latest_download_date = arrow.get(latest_download["date_published"])

            return latest_download_date > date_updated

        else:
            return False

    def update(
        self, downloaded_mod: DownloadResult, version: Version, loader: Loaders
    ) -> Optional[DownloadResult]:
        slug = downloaded_mod.slug
        site = downloaded_mod.source

        if site == Sites.Curseforge:
            return self.curse_api.download(slug, version, loader)

        if site == Sites.Modrinth:
            return self.modrinth_api.download(slug, version, loader)
