from ml.ml40.features.functionalities.functionality import Functionality
from ml.ml40.features.properties.values.documents.jobs.job import Job


class ClearsJobs(Functionality):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)

    def clear(self, job: Job) -> bool:
        pass
