from ml.ml40.features.functionalities.functionality import Functionality


class ProvidesWeatherData(Functionality):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)

