"""This module implements the class Cuts."""

from ml.ml40.features.functionalities.functionality import Functionality


class Cuts(Functionality):
    def __init__(self, name="", identifier=""):
        """Initializes the object.

        :param name: Object name
        :param identifier: Identifier

        """
        super().__init__(
            name=name,
            identifier=identifier)

    def cut(self):
        pass
