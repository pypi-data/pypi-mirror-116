from datetime import date

import pytest

from hijri_converter import convert


def test_importing_at_init_module():
    from hijri_converter import Gregorian, Hijri

    assert Hijri(1410, 8, 13).datetuple() == (1410, 8, 13)
    assert Gregorian(1990, 3, 10).datetuple() == (1990, 3, 10)


@pytest.fixture(scope="module")
def hijri():
    return convert.Hijri(1410, 8, 13)


@pytest.fixture(scope="module")
def gregorian():
    return convert.Gregorian(1990, 3, 10)


def test_hijri_representation(hijri):
    assert hijri.__repr__() == "Hijri(1410, 8, 13)"


def test_hijri_string_representation(hijri):
    assert hijri.__str__() == "1410-08-13"


def test_hijri_hash(hijri):
    assert hijri.__hash__() == hash(("Hijri", 1410, 8, 13))


@pytest.mark.parametrize("test_input", ["__gt__", "__ge__", "__lt__", "__le__"])
def test_hijri_comparison_notimplemented(hijri, test_input):
    assert getattr(hijri, test_input)("1410-08-13") == NotImplemented


def test_hijri_equality(hijri):
    assert hijri == convert.Hijri(1410, 8, 13)
    assert hijri != convert.Hijri(1410, 8, 14)
    assert hijri != "1410-08-13"


def test_hijri_ordering(hijri):
    assert hijri > convert.Hijri(1410, 8, 12)
    assert hijri >= convert.Hijri(1410, 8, 13)
    assert hijri < convert.Hijri(1410, 8, 14)
    assert hijri <= convert.Hijri(1410, 8, 13)


def test_hijri_fromisoformat(hijri):
    assert convert.Hijri.fromisoformat("1410-08-13") == hijri


def test_hijri_today(hijri):
    assert convert.Hijri.today().to_gregorian().isoformat() == date.today().isoformat()


def test_hijri_year(hijri):
    assert hijri.year == 1410


def test_hijri_month(hijri):
    assert hijri.month == 8


def test_hijri_day(hijri):
    assert hijri.day == 13


def test_hijri_datetuple(hijri):
    assert hijri.datetuple() == (1410, 8, 13)


def test_hijri_isoformat(hijri):
    assert hijri.isoformat() == "1410-08-13"


def test_hijri_dmyformat(hijri):
    assert hijri.dmyformat() == "13/08/1410"
    assert hijri.dmyformat(padding=False) == "13/8/1410"
    assert hijri.dmyformat(separator=".") == "13.08.1410"


def test_hijri_month_length(hijri):
    assert hijri.month_length() == 29


def test_hijri_month_name(hijri):
    assert hijri.month_name() == "Sha’ban"
    assert hijri.month_name("en") == "Sha’ban"
    assert hijri.month_name("en-US") == "Sha’ban"


def test_hijri_weekday(hijri):
    assert hijri.weekday() == 5


def test_hijri_iso_weekday(hijri):
    assert hijri.isoweekday() == 6


def test_hijri_day_name(hijri):
    assert hijri.day_name() == "Saturday"
    assert hijri.day_name("en") == "Saturday"
    assert hijri.day_name("en-US") == "Saturday"


def test_hijri_notation(hijri):
    assert hijri.notation() == "AH"
    assert hijri.notation("en") == "AH"
    assert hijri.notation("en-US") == "AH"


def test_hijri_to_julian(hijri):
    assert hijri.to_julian() == 2447961


def test_hijri_to_gregorian(hijri):
    assert hijri.to_gregorian().datetuple() == (1990, 3, 10)


def test_hijri_month_index(hijri):
    assert hijri._month_index() == 811


@pytest.mark.parametrize("test_input", [(1410, 9, 30), (1356, 1, 1), (1500, 12, 30)])
def test_hijri_valid_date(test_input):
    year, month, day = test_input
    try:
        convert.Hijri(year, month, day, validate=False)._check_date()
    except (ValueError, OverflowError):
        pytest.fail()


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ((37, 12, 30), "date out of range"),
        ((1342, 12, 29), "date out of range"),
        ((1501, 1, 1), "date out of range"),
    ],
)
def test_hijri_invalid_year(test_input, expected):
    with pytest.raises(OverflowError) as e:
        convert.Hijri(*test_input, validate=False)._check_date()
    assert str(e.value) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ((1410, 0, 1), "month must be in 1..12"),
        ((1410, 13, 1), "month must be in 1..12"),
        ((1410, 8, 30), "day must be in 1..29 for month"),
    ],
)
def test_hijri_invalid_day_or_month(test_input, expected):
    with pytest.raises(ValueError) as e:
        convert.Hijri(*test_input, validate=False)._check_date()
    assert str(e.value) == expected


def test_gregorian_fromdate():
    test_date = date(2014, 12, 28)
    assert convert.Gregorian.fromdate(test_date).datetuple() == (2014, 12, 28)


def test_gregorian_datetuple(gregorian):
    assert gregorian.datetuple() == (1990, 3, 10)


def test_gregorian_dmyformat(gregorian):
    assert gregorian.dmyformat() == "10/03/1990"
    assert gregorian.dmyformat(padding=False) == "10/3/1990"
    assert gregorian.dmyformat(separator=".") == "10.03.1990"


def test_gregorian_month_name(gregorian):
    assert gregorian.month_name() == "March"
    assert gregorian.month_name("en") == "March"
    assert gregorian.month_name("en-US") == "March"


def test_gregorian_day_name(gregorian):
    assert gregorian.day_name() == "Saturday"
    assert gregorian.day_name("en") == "Saturday"
    assert gregorian.day_name("en-US") == "Saturday"


def test_gregorian_notation(gregorian):
    assert gregorian.notation() == "CE"
    assert gregorian.notation("en") == "CE"
    assert gregorian.notation("en-US") == "CE"


def test_gregorian_to_julian(gregorian):
    assert gregorian.to_julian() == 2447961


def test_gregorian_to_hijri(gregorian):
    assert gregorian.to_hijri().datetuple() == (1410, 8, 13)


@pytest.mark.parametrize("test_input", [(1990, 3, 10), (1924, 8, 1), (2077, 11, 16)])
def test_gregorian_valid_range(test_input):
    year, month, day = test_input
    try:
        convert.Gregorian(year, month, day)._check_range()
    except OverflowError:
        pytest.fail()


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ((1924, 7, 31), "date out of range"),
        ((2077, 11, 17), "date out of range"),
    ],
)
def test_gregorian_invalid_range(test_input, expected):
    with pytest.raises(OverflowError) as e:
        convert.Gregorian(*test_input)._check_range()
    assert str(e.value) == expected
