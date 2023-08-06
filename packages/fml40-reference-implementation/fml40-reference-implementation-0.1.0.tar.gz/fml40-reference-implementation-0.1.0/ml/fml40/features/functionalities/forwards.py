"""This module implements the class Forwards."""

from ml.ml40.features.functionalities.functionality import Functionality
from ml.fml40.features.properties.values.documents.jobs.forwarding_job import ForwardingJob


class Forwards(Functionality):
    """This functionality signalizes that ForwardingJobs can be processed."""
    def __init__(self, name="", identifier=""):
        """Initializes the object.

        :param name: Object name
        :param identifier: Identifier

        """
        super().__init__(
            name=name,
            identifier=identifier)

    def executeJob(self, job):
        """Executes the given job.

        :param job: Job to be executed
        """
        pass


    def from_json(self, json_obj):
        """Initalizes this object from json_object.

        :param json_obj: JSON representation of this object
        """
        super().from_json(json_obj)
