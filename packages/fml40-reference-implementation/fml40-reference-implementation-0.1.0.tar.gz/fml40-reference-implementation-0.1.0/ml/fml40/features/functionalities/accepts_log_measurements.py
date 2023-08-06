"""This module implements the class AcceptsLogMeasurements."""

from ml.ml40.features.functionalities.functionality import Functionality
from ml.fml40.features.properties.values.documents.reports.log_measurement import LogMeasurement


class AcceptsLogMeasurements(Functionality):
    """This functionality signalizes that LogMeasurements can be processed."""
    def __init__(self, name="", identifier=""):
        """Initializes the object.

        :param name:  Object name
        :param identifier: Identifier

        """
        super().__init__(
            name=name,
            identifier=identifier)

    def acceptLogMeasurement(self, log_measurement: LogMeasurement) -> bool:
        """Accepts the given LogMeasurement. Returns true if the job has been
        accepted, otherwise returns false.

        :param job: LogMeasurement to be accepted
        :rtype: bool

        """
        pass
