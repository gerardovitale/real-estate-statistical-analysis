from abc import ABC, abstractmethod, abstractproperty


class Builder(ABC):

    @abstractproperty
    def create_search_params(self):
        pass

    @abstractmethod
    def set_operation(self):
        pass

    @abstractmethod
    def set_propertyType(self):
        pass

    @abstractmethod
    def set_center(self):
        pass

    @abstractmethod
    def set_locale(self):
        pass
    
    @abstractmethod
    def set_distance(self):
        pass

    @abstractmethod
    def set_locationId(self):
        pass

    @abstractmethod
    def set_maxItems(self):
        pass
    
    @abstractmethod
    def set_numPage(self):
        pass
