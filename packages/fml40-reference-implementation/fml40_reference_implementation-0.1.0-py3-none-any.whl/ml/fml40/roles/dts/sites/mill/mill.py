from ml.ml40.roles.dts.sites.site import Site


class Mill(Site):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)
