from ml.ml40.features.functionalities.functionality import Functionality


class Grabs(Functionality):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)

    def close(self):
        pass

    def open(self):
        pass
