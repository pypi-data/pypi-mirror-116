from ml.ml40.features.properties.values.documents.jobs.job import Job


class ForwardingJob(Job):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)
