"""This module implements the class AcceptsForwardingJobs."""

from ml.ml40.features.functionalities.accepts_jobs import AcceptsJobs
from ml.fml40.features.properties.values.documents.jobs.forwarding_job import (
    ForwardingJob,
)
from ml.app_logger import APP_LOGGER


class AcceptsForwardingJobs(AcceptsJobs):
    """This functionality signalizes that ForwadingJobs can be processed."""
    def __init__(self, name="", identifier=""):
        """Initializes the object.

        :param name:  Object name
        :param identifier: Identifier

        """
        super().__init__(
            name=name,
            identifier=identifier)

    def acceptJob(self, job: ForwardingJob) -> bool:
        """Accepts the given ForwardingJob. Returns true if the job has been
        accepted, otherwise returns false.

        :param job: ForwardingJob to be accepted
        :rtype: bool

        """
        pass
