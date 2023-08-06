from ml.ml40.features.functionalities.functionality import Functionality
from ml.ml40.features.properties.values.documents.reports.report import Report


class ProvidesOperationalData(Functionality):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)

    def getOperationalData(self) -> Report:
        return "this is a simply report"


