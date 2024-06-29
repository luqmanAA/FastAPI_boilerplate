import json
from typing import Any

from starlette.responses import JSONResponse


class CJSONResponse(JSONResponse):

    def render(self, content: Any) -> bytes:
        if isinstance(content, list):
            self.status_code = content[0]
            content = content[1]
        try:
            if not content['errors']:
                content.pop('errors')

            if content['data'] is None:
                content.pop('data')
        except (IndexError, TypeError, KeyError):
            pass

        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")
