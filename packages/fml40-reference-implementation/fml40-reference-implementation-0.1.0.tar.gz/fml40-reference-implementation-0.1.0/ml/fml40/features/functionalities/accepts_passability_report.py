from ml.ml40.features.functionalities.functionality import Functionality
from ml.fml40.features.properties.values.documents.reports.passability_report import PassabilityReport


class AcceptsPassabilityReport(Functionality):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)

    def acceptsReport(self, report:PassabilityReport):
        pass
