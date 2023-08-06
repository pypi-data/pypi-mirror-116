from ml.ml40.features.properties.values.value import Value


class DBH(Value):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)
        self.__dbh = None
        self.__json_out = dict()

    @property
    def dbh(self):
        return self.__dbh

    @dbh.setter
    def dbh(self, value):
        self.__dbh = value

    def to_json(self):
        self.__json_out = super().to_json()
        if self.dbh is not None:
            self.__json_out["dbh"] = self.dbh
        return self.__json_out