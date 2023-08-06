from ml.ml40.features.properties.values.documents.document import Document


class Report(Document):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)