"""This module implements the class AcceptsProximityAlert."""

from ml.ml40.features.functionalities.functionality import Functionality

class AcceptsProximityAlert(Functionality):
    """This functionality signalizes that an alert is generated if things
    are to close to this thing."""
    def __init__(self, name="", identifier=""):
        """Initializes the object.

        :param name:  Object name
        :param identifier: Identifier

        """
        super().__init__(
            name=name,
            identifier=identifier)

    def proximityAlert(self, ids: list, distances: list):
        print("Making Proximity Alert...")
