from ml.ml40.features.functionalities.functionality import Functionality


class ProvidesPassabilityInformation(Functionality):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)


    def calculatePassability(self, load, moisture):
        pass
