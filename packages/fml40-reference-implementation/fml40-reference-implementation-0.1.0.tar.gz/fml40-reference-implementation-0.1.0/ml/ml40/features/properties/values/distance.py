from ml.ml40.features.properties.values.value import Value


class Distance(Value):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)
        self.__distance = None

    @property
    def distance(self):
        return self.__distance

    @distance.setter
    def distance(self, value):
        self.__distance = value

    def to_json(self):
        self.__json_out = super().to_json()
        if self.__distance is not None:
            self.__json_out["distance"] = self.__distance
        return self.__json_out