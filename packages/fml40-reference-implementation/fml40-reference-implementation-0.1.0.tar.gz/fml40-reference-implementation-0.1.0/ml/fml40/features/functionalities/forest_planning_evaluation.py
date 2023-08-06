"""This module implements the class ForestPlanningEvaluation."""

from ml.ml40.features.functionalities.functionality import Functionality


class ForestPlanningEvaluation(Functionality):
    def __init__(self, name="", identifier=""):
        """Initializes the object.

        :param name: Object name
        :param identifier: Identifier

        """
        super().__init__(
            name=name,
            identifier=identifier)

    def evaluateInventoryData(self):
        pass
