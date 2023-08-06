from ml.ml40.features.properties.values.value import Value


class HarvestedVolume(Value):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)

        self.__volume = None
        self.__json_out = None

    @property
    def volume(self):
        return self.__volume

    @volume.setter
    def volume(self, value):
        self.__volume = value

    def to_json(self):
        self.__json_out = super().to_json()
        if self.volume is not None:
            self.__json_out["volume"] = self.volume
        return self.__json_out
