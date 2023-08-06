from ml.ml40.features.functionalities.functionality import Functionality
from ml.mml40.features.properties.values.Stretch import Stretch


class ProvidesStretchData(Functionality):

    def __init__(self, name="", identifier=""):
        """Initializes the object.

        :param name: Object name
        :param identifier: Identifier

        """
        super().__init__(
            name=name,
            identifier=identifier)

    def getStretchData(self, time) -> Stretch:
        pass

    def getStretchDataSeries(self, startTime, endTime):
        pass

    def getMaxStretch(self) -> Stretch:
        pass

    def getMinStretch(self) -> Stretch:
        pass
