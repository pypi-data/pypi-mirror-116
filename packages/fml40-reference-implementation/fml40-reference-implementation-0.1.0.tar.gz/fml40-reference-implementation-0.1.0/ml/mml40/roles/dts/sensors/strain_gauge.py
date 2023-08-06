from ml.ml40.roles.dts.sensors.sensor import Sensor


class StrainGauge(Sensor):
    def __init__(self, name="", identifier=""):
        super(StrainGauge, self).__init__(
            name=name,
            identifier=identifier)
