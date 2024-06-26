import pytest
from lec5_module import Field,  Drunk, UsualDrunk, Location

def test16_field():
    # Test adding a drunk
    f = Field()
    d = Drunk("Bob")
    loc = Location(0, 0)
    e = Drunk("Sam")
    des = Location(0, 3)
    f.add_drunk(d, loc)
    f.add_drunk(e, des)
    assert f.get_loc(d) == loc
    assert f.get_loc(e) == des

    # Test moving a drunk
    d.take_step = lambda: (1, 0)
    f.move_drunk(d)
    assert f.get_loc(d).get_x() == 1

    # Test adding a duplicate drunk
    try:
        f.add_drunk(d, loc)
    except ValueError as e:
        assert str(e) == "Duplicate drunk"

    # Test moving a drunk not in the field
    d2 = Drunk("Alice")
    try:
        f.move_drunk(d2)
    except ValueError as e:
        assert str(e) == "Drunk not in field"
