from ml.ml40.features.properties.values.value import Value


class OperatingHours(Value):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)

        self.__total = None
        self.__json_out = dict()

    @property
    def total(self):
        return self.__total

    @total.setter
    def total(self, value):
        self.__total = value

    def to_json(self):
        self.__json_out = super().to_json()
        if self.__total is not None:
            self.__json_out["total"] = self.__total
        return self.__json_out
