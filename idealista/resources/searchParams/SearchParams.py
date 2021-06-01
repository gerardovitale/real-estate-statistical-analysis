from typing import Any

from idealista.resources.searchParams.Builder import Builder


class SearchParams:

    def __init__(self) -> None:
        self.params = {}
        self._operation = None
        self._propertyType = None
        self._center = None
        self._locale = None
        self._distance = None
        self._locationId = None
        self._maxItems = None
        self._numPage = None

    def add(self, param_key: str, param_value: Any) -> None:
        self.params[param_key] = param_value
