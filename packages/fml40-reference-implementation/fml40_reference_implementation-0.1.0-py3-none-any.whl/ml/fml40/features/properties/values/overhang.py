from ml.ml40.features.properties.values.value import Value


class Overhang(Value):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)
        self.__overhang = None
        self.__json_out = dict()

    @property
    def overhang(self):
        return self.__overhang

    @overhang.setter
    def overhang(self, value):
        self.__overhang = value

    def to_json(self):
        self.__json_out = super().to_json()
        if self.overhang is not None:
            self.__json_out["overhang"] = self.__overhang
        return self.__json_out