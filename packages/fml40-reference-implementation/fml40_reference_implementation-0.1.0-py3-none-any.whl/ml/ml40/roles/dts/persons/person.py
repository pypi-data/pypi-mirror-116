from ml.ml40.roles.dts.dt import DT


class Person(DT):
    def __init__(self, name="", identifier=""):
        super(Person, self).__init__(
            name=name,
            identifier=identifier)