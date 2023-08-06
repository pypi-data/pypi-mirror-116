from ml.ml40.roles.dts.parts.part import Part


class Engine(Part):
    def __init__(self, name="", identifier=""):
        super(Engine, self).__init__(
            name=name,
            identifier=identifier)
