from ml.role import Role


class Service(Role):
    def __init__(self, name="", identifier=""):
        super(Service, self).__init__(
            name=name,
            identifier=identifier)