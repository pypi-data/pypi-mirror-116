from ml.ml40.features.functionalities.functionality import Functionality
from ml.ml40.features.properties.values.documents.reports.report import Report


class AcceptsReports(Functionality):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)

    def acceptReport(self, report: Report):
        pass
