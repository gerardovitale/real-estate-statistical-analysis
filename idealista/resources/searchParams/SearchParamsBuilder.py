from idealista.resources.searchParams.SearchParams import SearchParams
from idealista.resources.searchParams.Builder import Builder


class SearchParamsBuilder(Builder):

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._search_params = SearchParams()

    @property
    def create_search_params(self) -> SearchParams:
        search_params = self._search_params
        self.reset()
        return search_params

    def set_operation(self, operation):
        self._search_params._operation = operation
        self._search_params.add(param_key='operation', param_value=operation)
        return self

    def set_propertyType(self, propertyType):
        self._search_params._propertyType = propertyType
        self._search_params.add(param_key='propertyType', param_value=propertyType)
        return self
        
    def set_center(self, center):
        self._search_params._center = center
        self._search_params.add(param_key='center', param_value=center)
        return self
        
    def set_locale(self, locale):
        self._search_params._locale = locale
        self._search_params.add(param_key='locale', param_value=locale)
        return self
        
    def set_distance(self, distance):
        self._search_params._distance = distance
        self._search_params.add(param_key='distance', param_value=distance)
        return self
        
    def set_locationId(self, locationId):
        self._search_params._locationId = locationId
        self._search_params.add(param_key='locationId', param_value=locationId)
        return self
        
    def set_maxItems(self, maxItems):
        self._search_params._maxItems = maxItems
        self._search_params.add(param_key='maxItems', param_value=maxItems)
        return self
        
    def set_numPage(self, numPage):
        self._search_params._numPage = numPage
        self._search_params.add(param_key='numPage', param_value=numPage)
        return self
        