"""This module implements the class ClassifiesTreeSpecies."""

from ml.ml40.features.functionalities.functionality import Functionality


class ClassifiesTreeSpecies(Functionality):
    """This functionality allows the classification of tree species."""
    def __init__(self, name="", identifier=""):
        """Initializes the object.

        :param name:  Object name
        :param identifier: Identifier

        """
        super().__init__(
            name=name,
            identifier=identifier)

    def calculateTreeSpeciesClassification(self, tree: bytes) -> bytes:
        """Returns the classification of the species of tree.

        :param: tree: Specification of tree
        :return: Tree species
        :rtype: bytes
        """
        pass
