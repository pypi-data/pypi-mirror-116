from ml.ml40.features.functionalities.functionality import Functionality
from ml.ml40.features.properties.values.documents.jobs.job import Job
from ml.ml40.features.properties.values.documents.jobs.job_status import JobStatus
from ml.identifier import ID


class AcceptsJobs(Functionality):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)

    def acceptJob(self, job: Job) -> bool:
        pass

    def queryJobStatus(self, identifier: ID) -> JobStatus:
        pass

    def removeJob(self, identifier: ID) -> bool:
        pass
