from ml.fml40.roles.dts.sites.mill.mill import Mill


class Sawmill(Mill):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)
