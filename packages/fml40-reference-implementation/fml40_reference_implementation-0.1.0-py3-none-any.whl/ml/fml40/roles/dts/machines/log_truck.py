from ml.fml40.roles.dts.machines.forest_machine import ForestMachine


class LogTruck(ForestMachine):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)
