from ml.ml40.features.properties.values.documents.jobs.job import Job


class LogTransportationJob(Job):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)
        self.__woodPiles = []

    @property
    def woodPiles(self):
        return self.__woodPiles

    @woodPiles.setter
    def woodPiles(self, value):
        self.__woodPiles.append(value)

