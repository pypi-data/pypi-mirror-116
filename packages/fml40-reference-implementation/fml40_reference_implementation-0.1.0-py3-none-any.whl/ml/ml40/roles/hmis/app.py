from ml.ml40.roles.hmis.hmi import HMI


class App(HMI):
    def __init__(self, name="", identifier=""):
        super(App, self).__init__(
            name=name,
            identifier=identifier)