from ml.ml40.roles.dts.sensors.sensor import Sensor


class SoilSensor(Sensor):
    def __init__(self, name="", identifier=""):
        super(SoilSensor, self).__init__(
            name=name,
            identifier=identifier)