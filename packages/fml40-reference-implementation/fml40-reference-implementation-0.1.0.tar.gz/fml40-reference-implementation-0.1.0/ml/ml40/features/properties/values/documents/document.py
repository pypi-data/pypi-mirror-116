from ml.ml40.features.properties.values.value import Value


class Document(Value):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)