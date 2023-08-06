"""This module implements the class AcceptsFellingSupportJobs."""

from ml.ml40.features.functionalities.accepts_jobs import AcceptsJobs
from ml.fml40.features.properties.values.documents.jobs.fellung_support_job import FellingSupportJob


class AcceptsFellingSupportJobs(AcceptsJobs):
    """This functionality signalizes that FellingSupportJobs can be
    processed."""

    def __init__(self, name="", identifier=""):
        """Initializes the object.

        :param name:  Object name
        :param identifier: Identifier

        """
        super().__init__(
            name=name,
            identifier=identifier)

    def acceptJob(self, job: FellingSupportJob) -> bool:
        """Accepts the given FellingSupportJob job. Returns true if the job
        has been accepted, otherwise returns false.

        :param job: FellingSupportJob to be accepted
        :rtype: bool
        """
        pass
