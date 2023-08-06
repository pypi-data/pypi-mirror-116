from ml.ml40.roles.dts.handheld_devices.handheld_device import HandheldDevice


class Chainsaw(HandheldDevice):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)
