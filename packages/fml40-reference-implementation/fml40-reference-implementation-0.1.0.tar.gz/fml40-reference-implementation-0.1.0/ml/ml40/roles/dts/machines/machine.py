from ml.ml40.roles.dts.dt import DT


class Machine(DT):
    def __init__(self, name="", identifier=""):
        super(DT, self).__init__(
            name=name,
            identifier=identifier)

