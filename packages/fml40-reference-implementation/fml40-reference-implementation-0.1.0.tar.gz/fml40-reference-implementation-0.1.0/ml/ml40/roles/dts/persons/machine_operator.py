from ml.ml40.roles.dts.persons.person import Person


class MachineOperator(Person):
    def __init__(self, name="", identifier=""):
        super(MachineOperator, self).__init__(
            name=name,
            identifier=identifier)
