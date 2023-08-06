from ml.ml40.features.properties.values.value import Value


class Moisture(Value):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)
        self.__humidity = None
        self.__join_out = dict()

    @property
    def humidity(self):
        return self.__humidity

    @humidity.setter
    def humidity(self, value):
        self.__humidity = value

    def to_json(self):
        self.__join_out = super().to_json()
        if self.humidity is not None:
            self.__join_out["humidity"] = self.humidity
        return self.__join_out
