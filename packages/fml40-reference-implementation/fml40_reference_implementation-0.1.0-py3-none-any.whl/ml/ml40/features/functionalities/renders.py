from ml.ml40.features.functionalities.functionality import Functionality
from ml.identifier import ID


class Renders(Functionality):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)

    def create3DVideo(self, identifier: ID) -> bytes:
        pass
