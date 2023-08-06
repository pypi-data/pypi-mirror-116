from ml.ml40.features.functionalities.functionality import Functionality
from ml.fml40.features.properties.values.documents.jobs.felling_job import FellingJob
from ml.app_logger import APP_LOGGER


class Harvests(Functionality):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)

    def executeJob(self, job: FellingJob):
        pass


