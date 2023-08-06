from ml.ml40.roles.hmis.hmi import HMI


class Dashboard(HMI):
    def __init__(self, name="", identifier=""):
        super(Dashboard, self).__init__(
            name=name,
            identifier=identifier)