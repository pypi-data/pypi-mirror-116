from ml.ml40.features.functionalities.functionality import Functionality
from ml.ml40.features.properties.values.documents.reports.production_data import ProductionData


class ProvidesProductionData(Functionality):
    def __init__(self, name="", identifier=""):
        super(ProvidesProductionData, self).__init__(
            name=name,
            identifier=identifier)

    def getProductionData(self) -> ProductionData:
        return "Production Data is huge"
