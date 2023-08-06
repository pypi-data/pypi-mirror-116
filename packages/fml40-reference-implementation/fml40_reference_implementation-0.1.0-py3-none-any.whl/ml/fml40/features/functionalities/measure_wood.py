from ml.ml40.features.functionalities.functionality import Functionality
from ml.fml40.features.properties.values.documents.reports.log_measurement import LogMeasurement


class MeasuresWood(Functionality):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)

    def measureLog(self) -> LogMeasurement:
        pass
