from ml.ml40.features.functionalities.functionality import Functionality
from ml.fml40.features.properties.values.documents.reports.passability_report import PassabilityReport


class ProvidesMapData(Functionality):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)

    def getMapData(self, map: int) -> PassabilityReport:
        pass
