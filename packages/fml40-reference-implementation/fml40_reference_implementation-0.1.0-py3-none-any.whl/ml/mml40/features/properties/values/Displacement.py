from ml.ml40.features.properties.values.value import Value


class Displacement(Value):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)
        self.__displacement = None

    @property
    def displacement(self):
        return self.__displacement

    @displacement.setter
    def displacement(self, value):
        self.__displacement = value

    def to_json(self):
        self.__json_out = super().to_json()
        if self.displacement is not None:
            self.__json_out["displacement"] = self.displacement

        return self.__json_out