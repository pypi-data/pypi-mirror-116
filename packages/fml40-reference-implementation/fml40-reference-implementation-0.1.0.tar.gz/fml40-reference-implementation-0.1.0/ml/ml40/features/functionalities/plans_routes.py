from ml.ml40.features.functionalities.functionality import Functionality
from ml.ml40.features.properties.values.route import Route
from ml.ml40.features.properties.values.location import Location

class PlansRoutes(Functionality):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)


    def planRoute(self, start: Location, goal: Location) -> Route:
        pass
