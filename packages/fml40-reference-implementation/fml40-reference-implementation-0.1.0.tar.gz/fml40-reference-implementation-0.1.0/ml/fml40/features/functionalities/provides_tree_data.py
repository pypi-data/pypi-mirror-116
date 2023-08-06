from ml.ml40.features.functionalities.functionality import Functionality
from ml.ml40.features.properties.values.location import Location
from ml.identifier import ID
from ml.fml40.features.properties.values.tree_data import TreeData


class ProvidesTreeData(Functionality):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)

    def getTreeData(self, Tree:ID) -> list:
        pass

    def getTreesInDiameter(self, location: Location, diameter: float) -> list:
        pass
