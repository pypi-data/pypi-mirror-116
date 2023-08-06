from ml.ml40.features.properties.values.documents.reports.report import Report


class SoilMoistureMeasurement(Report):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)