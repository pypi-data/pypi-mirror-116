"""This module implements the class GeneratesAfforestationSuggestions."""

from ml.ml40.features.functionalities.functionality import Functionality
from ml.identifier import ID


class GeneratesFellingSuggestions(Functionality):
    """This functionality can generate suggestions regarding how to fell a
    tree.
    """
    def __init__(self, name="", identifier=""):
        """Initializes the object.

        :param name: Object name
        :param identifier: Identifier

        """
        super().__init__(
            name=name,
            identifier=identifier)

    def generateFellingSuggestion(self, tree_Id: ID):
        """Returns a suggestion regarding how to fell a tree.

        :param: tree_Id: Identifier of a tree
        """
        pass
