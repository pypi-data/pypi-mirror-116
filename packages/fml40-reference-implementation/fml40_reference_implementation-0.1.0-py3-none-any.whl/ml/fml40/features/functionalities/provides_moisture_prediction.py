from ml.ml40.features.functionalities.functionality import Functionality
from ml.fml40.features.properties.values.documents.reports.passability_report import PassabilityReport


class ProvidesMoisturePrediction(Functionality):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)

    def predict(self):
        pass

    def predictMoistures(self, location, moisture):
        pass
