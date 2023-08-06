from ml.ml40.features.properties.values.value import Value


class Assortment(Value):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)
        self.__grade = None
        self.__json_out = dict()

    @property
    def grade(self):
        return self.__grade

    @grade.setter
    def grade(self, value):
        self.__grade = value

    def to_json(self):
        self.__json_out = super().to_json()
        if self.grade is not None:
            self.__json_out["grade"] = self.grade

        return self.__json_out
