from ml.ml40.roles.dts.dt import DT


class Site(DT):
    def __init__(self, name="", identifier=""):
        super(Site, self).__init__(
            name=name,
            identifier=identifier)