class ParkingPermit:
    """A parking permit with an owner, a number of months and a fee schedule"""

    def __init__(self, owner: str, months: int, fees: dict[str, float]) -> None:
        """Create a new permit

        Parameters: owner - the owner's name; months - months purchased; fees - the fee schedule
        Precondition: months >= 0 and fees has a 'monthly' key
        """
        self.owner = owner
        self.months = months
        self.fees = fees

    def cost(self) -> float:
        """Return the base cost: months * the monthly fee"""
        return self.months * self.fees['monthly']

    def __str__(self) -> str:
        """Return the permit as a readable string"""
        return 'Parking permit for ' + self.owner + ': ' + str(self.months) + ' months, $' + str(self.cost())

    def __repr__(self) -> str:
        """Return the permit as a constructor call"""
        return 'ParkingPermit(' + repr(self.owner) + ', ' + str(self.months) + ', ' + repr(self.fees) + ')'


class StudentPermit(ParkingPermit):
    """A student parking permit that also stores the number of vehicles"""

    def __init__(self, owner: str, months: int, fees: dict[str, float], vehicles: int) -> None:
        """Create a new student permit

        Parameters: owner, months, fees - same as ParkingPermit; vehicles - number of vehicles registered
        Precondition: vehicles >= 1 and fees has 'monthly' and 'extra_vehicle' keys
        """
        super().__init__(owner, months, fees)
        self.vehicles = vehicles

    def cost(self) -> float:
        """Return the monthly cost plus a one-time fee for each vehicle after the first"""
        extra_vehicles = max(self.vehicles - 1, 0)
        return super().cost() + extra_vehicles * self.fees['extra_vehicle']

    def __str__(self) -> str:
        """Return the permit as a readable string"""
        return ('Student permit for ' + self.owner + ': ' + str(self.months) + ' months, '
                + str(self.vehicles) + ' vehicles, $' + str(self.cost()))

    def __repr__(self) -> str:
        """Return the permit as a constructor call"""
        return ('StudentPermit(' + repr(self.owner) + ', ' + str(self.months) + ', '
                + repr(self.fees) + ', ' + str(self.vehicles) + ')')


class FacultyPermit(ParkingPermit):
    """A faculty parking permit that also stores if garage access is included"""

    def __init__(self, owner: str, months: int, fees: dict[str, float], garage: bool) -> None:
        """Create a new faculty permit

        Parameters: owner, months, fees - same as ParkingPermit; garage - True if garage access is included
        Precondition: fees has 'monthly' and 'garage' keys
        """
        super().__init__(owner, months, fees)
        self.garage = garage

    def cost(self) -> float:
        """Return the monthly cost plus the monthly garage fee if garage access is included"""
        total = super().cost()
        if self.garage:
            total += self.months * self.fees['garage']
        return total

    def __str__(self) -> str:
        """Return the permit as a readable string"""
        if self.garage:
            garage_text = 'with garage'
        else:
            garage_text = 'no garage'
        return ('Faculty permit for ' + self.owner + ': ' + str(self.months) + ' months, '
                + garage_text + ', $' + str(self.cost()))

    def __repr__(self) -> str:
        """Return the permit as a constructor call"""
        return ('FacultyPermit(' + repr(self.owner) + ', ' + str(self.months) + ', '
                + repr(self.fees) + ', ' + str(self.garage) + ')')


def main() -> None:
    """Create a few permits and print them"""
    student_fees = {'monthly': 25, 'extra_vehicle': 10}
    faculty_fees = {'monthly': 40, 'garage': 15}

    permits = [
        StudentPermit('Ann', 6, student_fees, 1),
        StudentPermit('Bob', 6, student_fees, 3),
        FacultyPermit('Dr. Smith', 12, faculty_fees, False),
        FacultyPermit('Dr. Jones', 12, faculty_fees, True),
    ]

    for permit in permits:
        print(permit)
        print(repr(permit))


if __name__ == '__main__':
    main()
