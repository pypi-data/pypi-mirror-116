from abc import ABC


class AbstractInventory(ABC):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)
