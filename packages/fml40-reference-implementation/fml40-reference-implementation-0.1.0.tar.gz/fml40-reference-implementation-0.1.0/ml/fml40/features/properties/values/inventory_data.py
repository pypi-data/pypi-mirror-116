from ml.fml40.features.properties.values.abstract_inventory import AbstractInventory
from ml.ml40.features.properties.values.value import Value


class InventoryData(Value):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)

        self.__data = []
        self.__json_out = dict()

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data = value

    def to_json(self):
        self.__json_out = super().to_json()
        if self.data:
            self.__json_out["data"] = self.data
        return self.__json_out

