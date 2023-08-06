from ml.ml40.features.properties.values.value import Value


class Count(Value):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)
        self.currentCount = None
        self.maxCount = None
        self.minCount = None
        self.__json_out = dict()

    def to_json(self):
        self.__json_out = super().to_json()
        if self.currentCount is not None:
            self.__json_out["currentCount"] = self.currentCount
        if self.maxCount is not None:
            self.__json_out["maxCount"] = self.maxCount
        if self.minCount is not None:
            self.__json_out["minCount"] = self.minCount

        return self.__json_out
