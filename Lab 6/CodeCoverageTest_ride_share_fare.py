"""Lab 6 - Step 5: test cases written for LINE (code) coverage of ride_share_fare.py.

Run:
    coverage run -m pytest CodeCoverageTest_ride_share_fare.py
    coverage report -m
"""
import pytest
from ride_share_fare import extra_distance_fare, seats_and_bags_ok, pickup_status


# ---------- extra_distance_fare ----------
def test_within_included_distance():
    # sedan includes 8 km, 5 km is inside it -> extra <= 0 -> fare 0
    assert extra_distance_fare("sedan", 5, "city", False) == 0


def test_unknown_cab_type_raises():
    with pytest.raises(ValueError, match="unknown cab type"):
        extra_distance_fare("bike", 5, "city", False)


def test_negative_distance_raises():
    with pytest.raises(ValueError, match="invalid distance"):
        extra_distance_fare("mini", -1, "city", False)


def test_subscriber_gets_three_extra_km():
    # sedan 8 + 3 = 11 included, 15 km -> extra 4 km at city rate 12 -> 48
    assert extra_distance_fare("sedan", 15, "city", True) == 48


def test_city_normal_rate():
    # mini includes 5 km, 15 km -> extra 10 at 12 -> 120
    assert extra_distance_fare("mini", 15, "city", False) == 120


def test_outstation_normal_rate():
    # extra 10 at 18 -> 180
    assert extra_distance_fare("mini", 15, "outstation", False) == 180


def test_long_outstation_trip_has_surcharges():
    # extra 25 km: rate 18 + 8 + 4 = 30 -> 750
    assert extra_distance_fare("mini", 30, "outstation", False) == 750


# ---------- seats_and_bags_ok ----------
def test_seats_and_bags_ok():
    assert seats_and_bags_ok(2, 1, False) is True


def test_wheelchair_with_two_passengers():
    assert seats_and_bags_ok(2, 0, True) is True


def test_too_many_passengers():
    assert seats_and_bags_ok(5, 0, False) is False


# ---------- pickup_status ----------
def test_pickup_on_time():
    assert pickup_status(10, True, False) == "on_time"


def test_pickup_delayed():
    assert pickup_status(0, True, False) == "delayed"


def test_pickup_missed():
    assert pickup_status(-20, False, False) == "missed"


def test_airport_adds_ten_minutes_to_cutoff():
    # unscheduled airport cutoff = 5 + 10 = 15 -> 15 minutes early is on time
    assert pickup_status(15, False, True) == "on_time"
