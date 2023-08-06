from ml.ml40.features.properties.values.value import Value


class LastServiceCheck(Value):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)

        self.__timestamp = None
        self.__json_out = dict()

    @property
    def timestamp(self):
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, value):
        self.__timestamp = value

    def to_json(self):
        self.__json_out = super().to_json()
        if self.__timestamp is not None:
            self.__json_out["weight"] = self.__timestamp
        return self.__json_out

