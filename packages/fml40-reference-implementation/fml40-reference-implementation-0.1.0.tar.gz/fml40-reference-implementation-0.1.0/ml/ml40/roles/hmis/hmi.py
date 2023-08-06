from ml.role import Role


class HMI(Role):
    def __init__(self, name="", identifier=""):
        super(HMI, self).__init__(
            name=name,
            identifier=identifier)
