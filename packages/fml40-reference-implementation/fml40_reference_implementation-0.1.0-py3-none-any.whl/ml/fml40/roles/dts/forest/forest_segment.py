from ml.fml40.roles.dts.forest.forest import Forest


class ForestSegment(Forest):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)
