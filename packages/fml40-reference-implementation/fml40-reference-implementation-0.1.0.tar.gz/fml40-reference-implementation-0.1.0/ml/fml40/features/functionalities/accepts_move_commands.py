"""This module implements the class AcceptsMoveCommands."""

from ml.ml40.features.functionalities.functionality import Functionality

class AcceptsMoveCommands(Functionality):
    """This functionality signalizes that the thing can be moved remotely
    via S3I-B messages ."""
    def __init__(self, name="", identifier=""):
        """Initializes the object.

        :param name:  Object name
        :param identifier: Identifier

        """
        super().__init__(
            name=name,
            identifier=identifier)

    def move(self, longitude: float, latitude: float):
        """Moves the thing to the position specified longitude and latitude.

        :param longitude: Longitude
        :param latitude: Latitude

        """
        print("move to longitude: {}, latitude : {}".format(longitude, latitude))
        return {"longitude": longitude, "latitude": latitude}
