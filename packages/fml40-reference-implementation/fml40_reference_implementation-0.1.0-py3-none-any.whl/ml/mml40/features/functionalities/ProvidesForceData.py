from ml.ml40.features.functionalities.functionality import Functionality
from ml.ml40.features.properties.values.force import Force


class ProvidesForceData(Functionality):
    def __init__(self, name="", identifier=""):
        """Initializes the object.

        :param name: Object name
        :param identifier: Identifier

        """
        super().__init__(
            name=name,
            identifier=identifier)

    def compileForceWithMaterial(self, stretchData, materialType) -> [Force]:
        pass

    def compileForceWithGeometry(self, stretchData, geometryType) -> [Force]:
        pass

    def getMaxForce(self) -> Force:
        pass

    def getMinForce(self) -> Force:
        pass

    def getForceData(self, time) -> Force:
        pass

    def getForceDataSeries(self, startTime, endTime) -> [Force]:
        pass

