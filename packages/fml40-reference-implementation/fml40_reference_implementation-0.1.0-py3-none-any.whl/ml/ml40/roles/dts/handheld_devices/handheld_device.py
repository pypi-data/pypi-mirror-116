from ml.ml40.roles.dts.dt import DT


class HandheldDevice(DT):
    def __init__(self, name="", identifier=""):
        super(HandheldDevice, self).__init__(
            name=name,
            identifier=identifier)


