"""This module implements the class AcceptsSingleTreeFellingJobs."""

from ml.ml40.features.functionalities.accepts_jobs import AcceptsJobs


class AcceptsSingleTreeFellingJobs(AcceptsJobs):
    """This functionality signalizes that single trees can be felled."""
    def __init__(self, name="", identifier=""):
        """Initializes the object.

        :param name:  Object name
        :param identifier: Identifier

        """
        super().__init__(
            name=name,
            identifier=identifier)
