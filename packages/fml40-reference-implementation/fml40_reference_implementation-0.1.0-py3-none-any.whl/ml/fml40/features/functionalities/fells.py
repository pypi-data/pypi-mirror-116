"""This module implements the class Fells."""

from ml.ml40.features.functionalities.functionality import Functionality
from ml.fml40.features.properties.values.tree_data import TreeData
from ml.fml40.features.properties.values.documents.jobs.felling_job import FellingJob


class Fells(Functionality):
    """This functionality signalizes that FellingJobs can be processed and
    offers the possibility to fell trees."""
    def __init__(self, name="", identifier=""):
        """Initializes the object.

        :param name: Object name
        :param identifier: Identifier

        """
        super().__init__(
            name=name,
            identifier=identifier)

    def executeFellingJob(self, job: FellingJob):
        """Executes the given FellingJob.

        :param FellingJob: Specification of the job
        """
        print("i am executing the felling job {}".format(job))
        pass


    def fell(self, tree_data: TreeData):
        """Fells the tree specified by tree_data

        :param tree_data: Description of the tree.
        """
        print("i am felling the tree {}".format(tree_data))
        pass
