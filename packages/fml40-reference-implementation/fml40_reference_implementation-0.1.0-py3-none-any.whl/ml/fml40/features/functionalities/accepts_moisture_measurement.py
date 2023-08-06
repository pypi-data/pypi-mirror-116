"""This module implements the class AcceptsMoistureMeasurement."""

from ml.ml40.features.functionalities.functionality import Functionality
from ml.fml40.features.properties.values.documents.reports.soil_moisture_measurement import SoilMoistureMeasurement


class AcceptsMoistureMeasurement(Functionality):
    """This functionality signalizes that SoilMoistureMeasurements can be
    processed."""
    def __init__(self, name="", identifier=""):
        """Initializes the object.

        :param name:  Object name
        :param identifier: Identifier

        """
        super().__init__(
            name=name,
            identifier=identifier)

    def acceptMoistureMeasurement(self, input: SoilMoistureMeasurement):
        """Accepts the given SoilMoistureMeasurement.

        """
        pass
