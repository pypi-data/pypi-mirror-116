"""This module implements the class GeneratesAfforestationSuggestions."""

from ml.ml40.features.functionalities.functionality import Functionality
from ml.fml40.features.properties.values.documents.reports.afforestation_suggestion import AfforestationSuggestion


class GeneratesAfforestationSuggestions(Functionality):
    """This functionality can generate suggestions for afforestation."""
    def __init__(self, name="", identifier=""):
        """Initializes the object.

        :param name: Object name
        :param identifier: Identifier

        """
        super().__init__(
            name=name,
            identifier=identifier)

    def generateAfforestationSuggestion(self) -> AfforestationSuggestion:
        """Returns a suggestion for afforestation.

        :returns: Suggestion for afforestation
        :rtype: AfforestationSuggestion
        """
        pass
