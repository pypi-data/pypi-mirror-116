from ml.ml40.features.properties.values.value import Value

class Stretch(Value):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)

        self.__stretch = None

    @property
    def stretch(self):
        return  self.__stretch

    @stretch.setter
    def stretch(self, value):
        self.__stretch = value


    def to_json(self):
        self.__json_out = super().to_json()
        if self.__stretch is not None:
            self.__json_out["stretch"] = self.__stretch
        return self.__json_out
