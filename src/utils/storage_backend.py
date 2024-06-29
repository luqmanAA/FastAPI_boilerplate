from urllib.parse import urljoin

from src.config import MEDIA_URL


class Storage:
    BASE_URL: str = ""

    @property
    def media_storage(self):
        return urljoin(self.BASE_URL, MEDIA_URL)


storage = Storage()
