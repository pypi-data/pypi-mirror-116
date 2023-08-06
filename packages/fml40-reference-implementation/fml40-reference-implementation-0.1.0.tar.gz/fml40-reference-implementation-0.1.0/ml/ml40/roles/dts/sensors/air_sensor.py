from ml.ml40.roles.dts.sensors.sensor import Sensor


class AirSensor(Sensor):
    def __init__(self, name="", identifier=""):
        super(AirSensor, self).__init__(
            name=name,
            identifier=identifier)