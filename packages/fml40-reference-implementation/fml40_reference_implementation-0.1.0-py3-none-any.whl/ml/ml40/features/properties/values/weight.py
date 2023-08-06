from ml.ml40.features.properties.values.value import Value


class Weight(Value):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)

        self.__weight = None
        self.__json_out = dict()

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        self.__weight = value

    def to_json(self):
        self.__json_out = super().to_json()
        if self.weight is not None:
            self.__json_out["weight"] = self.weight
        return self.__json_out

