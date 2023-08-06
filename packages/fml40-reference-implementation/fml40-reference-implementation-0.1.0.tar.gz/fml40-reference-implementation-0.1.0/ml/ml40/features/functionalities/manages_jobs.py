from ml.ml40.features.functionalities.functionality import Functionality
from ml.ml40.features.properties.values.documents.jobs.job import Job
from ml.ml40.features.properties.values.documents.reports.report import Report
from ml.identifier import ID


class ManagesJobs(Functionality):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)

    def acceptReport(self, report: Report):
        pass

    def assignJob(self, job: Job, identifier: ID):
        pass
