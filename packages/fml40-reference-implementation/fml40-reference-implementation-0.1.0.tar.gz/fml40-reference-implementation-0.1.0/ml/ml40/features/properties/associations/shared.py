from ml.ml40.features.properties.associations.association import Association


class Shared(Association):
    def __init__(self, name="", identifier=""):
        super(Shared, self).__init__(
            name=name,
            identifier=identifier)
        self.__targets = []
        self.__targets = dict()
        self.__json_out = dict()

    @property
    def targets(self):
        return self.__targets

    @targets.setter
    def targets(self, value):
        self.__targets = value

    def to_json(self):
        self.__json_out = super().to_json()
        if self.targets:
            self.__json_out["targets"] = []
            for key in self.targets.keys():
                self.__json_out["targets"].append(self.targets[key].to_subthing_json())
        return self.__json_out
