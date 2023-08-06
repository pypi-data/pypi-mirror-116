from ml.ml40.roles.hmis.hmi import HMI


class MachineUI(HMI):
    def __init__(self, name="", identifier=""):
        super(MachineUI, self).__init__(
            name=name,
            identifier=identifier)