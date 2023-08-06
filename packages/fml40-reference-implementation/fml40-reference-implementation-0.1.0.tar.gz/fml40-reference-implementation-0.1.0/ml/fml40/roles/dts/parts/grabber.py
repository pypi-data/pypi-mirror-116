from ml.ml40.roles.dts.parts.part import Part


class Grabber(Part):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)
