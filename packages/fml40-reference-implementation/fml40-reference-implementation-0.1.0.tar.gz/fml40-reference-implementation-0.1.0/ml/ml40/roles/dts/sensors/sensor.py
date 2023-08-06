from ml.ml40.roles.dts.dt import DT


class Sensor(DT):
    def __init__(self, name="", identifier=""):
        super(Sensor, self).__init__(
            name=name,
            identifier=identifier)