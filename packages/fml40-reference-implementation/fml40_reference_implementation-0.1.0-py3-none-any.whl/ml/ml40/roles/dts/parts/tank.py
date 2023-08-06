from ml.ml40.roles.dts.parts.part import Part


class Tank(Part):
    def __init__(self, name="", identifier=""):
        super(Tank, self).__init__(
            name=name,
            identifier=identifier)