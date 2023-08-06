from ml.ml40.roles.dts.persons.person import Person


class ForestOwner(Person):
    def __init__(self, name="", identifier=""):
        super().__init__(
            name=name,
            identifier=identifier)
