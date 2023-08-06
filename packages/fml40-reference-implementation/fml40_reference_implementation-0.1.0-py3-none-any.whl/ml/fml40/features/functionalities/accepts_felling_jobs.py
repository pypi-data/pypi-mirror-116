"""This module implements the class AcceptsFellingJobs."""

from ml.ml40.features.functionalities.accepts_jobs import AcceptsJobs
from ml.ml40.features.properties.values.documents.jobs.job_status import JobStatus
from ml.fml40.features.properties.values.documents.jobs.felling_job import FellingJob


class AcceptsFellingJobs(AcceptsJobs):
    """This functionality signalizes that FellingJobs can be processed and
    offers the possibility to remove and query it."""

    def __init__(self, name="", identifier=""):
        """Initializes the object.

        :param name: Object name
        :param identifier: Identifier

        """
        super().__init__(
            name=name,
            identifier=identifier)

    def acceptJob(self, job: FellingJob) -> bool:
        """Accepts the given FellingJob job. Returns true if the job has been
        accepted, otherwise returns false.

        :param job: FellingJob to be accepted
        :rtype: bool

        """
        pass

    def queryJobStatus(self, identifier) -> JobStatus:
        """Returns the status of the job whose id is identical to identifier.

        :param identifier: Identifier of the job to be queried
        :returns: Status of the job
        :rtype: JobStatus

        """
        pass

    def removeJob(self, identifier) -> bool:
        """Removes the job with the id identical to identifier. Returns true
        if the job has been removed, otherwise returns false.

        :param identifier: Identifier of the job to be deleted
        :rtype: bool

        """
        pass
