from ml.ml40.features.functionalities.functionality import Functionality
from ml.fml40.features.properties.values.documents.jobs.log_transportation_job import LogTransportationJob
from ml.fml40.features.properties.values.documents.reports.log_transportation_report import LogTransportationReport


class TransportsLogs(Functionality):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)

    def transportLogs(self, job: LogTransportationJob) -> LogTransportationReport:
        print("i am making Log transportation report for the job {}".format(job))
        return "the transportation report is huge"
