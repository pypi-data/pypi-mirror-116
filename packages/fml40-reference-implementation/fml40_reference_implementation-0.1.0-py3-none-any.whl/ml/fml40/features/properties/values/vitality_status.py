from ml.ml40.features.properties.values.value import Value


class VitalityStatus(Value):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)
        self.__ok = None
        self.__json_out = dict()

    @property
    def ok(self):
        return self.__ok

    @ok.setter
    def ok(self, value):
        self.__ok = value

    def to_json(self):
        self.__json_out = super().to_json()
        if self.__ok is not None:
            self.__json_out["ok"] = self.__ok
        return self.__json_out
