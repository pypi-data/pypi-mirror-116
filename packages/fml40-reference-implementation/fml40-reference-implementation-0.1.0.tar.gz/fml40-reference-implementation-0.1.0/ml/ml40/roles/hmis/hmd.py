from ml.ml40.roles.hmis.hmi import HMI


class HMD(HMI):
    def __init__(self, name="", identifier=""):
        super(HMD, self).__init__(
            name=name,
            identifier=identifier)
