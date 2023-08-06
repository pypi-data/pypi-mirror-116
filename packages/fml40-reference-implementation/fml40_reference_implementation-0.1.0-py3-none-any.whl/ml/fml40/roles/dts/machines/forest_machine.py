from ml.ml40.roles.dts.machines.machine import Machine


class ForestMachine(Machine):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)