"""Lab 6 - Step 7: test cases written for BRANCH coverage of ride_share_fare.py.

Every if / elif is driven both True and False, including boundary values.

Run:
    coverage run --branch -m pytest BranchCoverageTest_ride_share_fare.py
    coverage report -m
"""
import pytest
from ride_share_fare import extra_distance_fare, seats_and_bags_ok, pickup_status


# ---------- extra_distance_fare ----------
# Branch: cab_type not in INCLUDED_KM  (True / False)
def test_unknown_cab_type_raises():
    with pytest.raises(ValueError, match="unknown cab type"):
        extra_distance_fare("bike", 5, "city", False)


# Branch: distance_km < 0  (True / False)
def test_negative_distance_raises():
    with pytest.raises(ValueError, match="invalid distance"):
        extra_distance_fare("mini", -1, "city", False)


def test_zero_distance_is_valid_and_free():
    assert extra_distance_fare("mini", 0, "city", False) == 0


# Branch: is_subscriber and cab_type != "suv"  (all three outcomes)
def test_subscriber_non_suv_gets_three_extra_km():
    # sedan 8 + 3 = 11 included; 15 km -> extra 4 * 12 = 48
    assert extra_distance_fare("sedan", 15, "city", True) == 48


def test_subscriber_suv_gets_no_bonus():
    # suv stays at 12 included; 20 km -> extra 8 * 12 = 96
    assert extra_distance_fare("suv", 20, "city", True) == 96


def test_non_subscriber_gets_no_bonus():
    # sedan 8 included; 15 km -> extra 7 * 12 = 84
    assert extra_distance_fare("sedan", 15, "city", False) == 84


# Branch: extra <= 0  (True / False, with boundaries)
def test_within_included_distance():
    assert extra_distance_fare("sedan", 5, "city", False) == 0


def test_exactly_included_distance_is_free():
    assert extra_distance_fare("mini", 5, "city", False) == 0


def test_one_km_over_included_is_charged():
    assert extra_distance_fare("mini", 6, "city", False) == 12


# Branch: zone == "city"  (True / False)
def test_city_rate():
    assert extra_distance_fare("mini", 15, "city", False) == 120


def test_non_city_rate():
    assert extra_distance_fare("mini", 15, "outstation", False) == 180


# Branch: extra > 20  (True / False, boundary 20 and 21) and zone == "outstation"
def test_extra_exactly_20_has_no_surcharge():
    # mini: 25 km -> extra 20 * 12 = 240
    assert extra_distance_fare("mini", 25, "city", False) == 240


def test_extra_21_city_gets_long_trip_surcharge_only():
    # extra 21 -> rate 12 + 8 = 20 -> 420
    assert extra_distance_fare("mini", 26, "city", False) == 420


def test_long_outstation_gets_both_surcharges():
    # extra 25 -> rate 18 + 8 + 4 = 30 -> 750
    assert extra_distance_fare("mini", 30, "outstation", False) == 750


def test_long_trip_in_other_zone_gets_no_outstation_surcharge():
    # zone neither city nor outstation: rate 18 + 8 = 26; extra 25 -> 650
    assert extra_distance_fare("mini", 30, "highway", False) == 650


# ---------- seats_and_bags_ok ----------
# Branch: needs_wheelchair  (True / False)
def test_wheelchair_two_passengers_ok():
    assert seats_and_bags_ok(2, 0, True) is True


def test_wheelchair_three_passengers_not_ok():
    assert seats_and_bags_ok(3, 0, True) is False


# Branch: passengers > 4  (True / False)
def test_five_passengers_not_ok():
    assert seats_and_bags_ok(5, 0, False) is False


def test_four_passengers_and_two_bags_ok():
    assert seats_and_bags_ok(4, 2, False) is True


def test_four_passengers_three_bags_not_ok():
    assert seats_and_bags_ok(4, 3, False) is False


def test_seats_and_bags_ok():
    assert seats_and_bags_ok(2, 1, False) is True


# ---------- pickup_status ----------
# Branches: is_scheduled, is_airport, minutes_early >= cutoff, >= cutoff - 15
def test_scheduled_on_time_boundary():
    assert pickup_status(10, True, False) == "on_time"


def test_scheduled_delayed_upper_boundary():
    assert pickup_status(9, True, False) == "delayed"


def test_scheduled_delayed_lower_boundary():
    assert pickup_status(-5, True, False) == "delayed"


def test_scheduled_missed_boundary():
    assert pickup_status(-6, True, False) == "missed"


def test_unscheduled_on_time_boundary():
    assert pickup_status(5, False, False) == "on_time"


def test_unscheduled_delayed_boundaries():
    assert pickup_status(4, False, False) == "delayed"
    assert pickup_status(-10, False, False) == "delayed"


def test_unscheduled_missed_boundary():
    assert pickup_status(-11, False, False) == "missed"


def test_scheduled_airport_cutoff_is_twenty():
    assert pickup_status(20, True, True) == "on_time"
    assert pickup_status(19, True, True) == "delayed"


def test_unscheduled_airport_cutoff_is_fifteen():
    assert pickup_status(15, False, True) == "on_time"
    assert pickup_status(0, False, True) == "delayed"
    assert pickup_status(-1, False, True) == "missed"
