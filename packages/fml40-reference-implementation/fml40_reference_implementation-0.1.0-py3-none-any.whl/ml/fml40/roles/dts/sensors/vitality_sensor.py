from ml.ml40.roles.dts.sensors.sensor import Sensor


class VitalitySensor(Sensor):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)
