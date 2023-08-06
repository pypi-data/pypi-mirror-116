from ml.ml40.features.properties.values.value import Value


class HarvestingParameters(Value):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)
        self.__cuttingLengths = None
        self.__json_out = dict()

    @property
    def cuttingLengths(self):
        return self.__cuttingLengths

    @cuttingLengths.setter
    def cuttingLengths(self, value):
        self.__cuttingLengths = value

    def to_json(self):
        self.__json_out = super().to_json()
        if self.cuttingLengths is not None:
            self.__json_out["cuttingLengths"] = self.cuttingLengths
        return self.__json_out
