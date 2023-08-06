from ml.ml40.features.functionalities.functionality import Functionality
from ml.mml40.features.properties.values.Displacement import Displacement


class ProvidesDisplacementData(Functionality):
    def __init__(self, name="", identifier=""):
        """Initializes the object.

        :param name: Object name
        :param identifier: Identifier

        """
        super().__init__(
            name=name,
            identifier=identifier)

    def compileDisplacementWithGeometry(self, stretchData, geometryType) -> [Displacement]:
        pass

    def compileDisplacementWithMaterial(self, stretchData, materialType) -> [Displacement]:
        pass

    def getMaxDisplacement(self) -> Displacement:
        pass

    def getMinDisplacement(self) -> Displacement:
        pass

    def getDisplacementData(self, time) -> [Displacement]:
        pass

    def getDisplacementDataSeries(self, startTime, endTime) -> [Displacement]:
        pass
