"""First pass: visit every line of the bike-share application."""

import pytest

from bike_share_rental import can_unlock, dock_status, ride_cost


def test_unknown_bike_is_rejected():
    with pytest.raises(ValueError, match="unknown bike type"):
        ride_cost("tandem", 30, False, False)


def test_zero_minutes_is_rejected():
    with pytest.raises(ValueError, match="invalid duration"):
        ride_cost("standard", 0, False, False)


def test_subscriber_gets_a_free_short_ride():
    assert ride_cost("standard", 30, True, False) == 0


def test_long_electric_ride_gets_peak_and_long_ride_fees():
    # 181 minutes rounds up to seven blocks: 7 * 35 + 15 + 100.
    assert ride_cost("electric", 181, False, True) == 360


def test_dock_rejects_zero_capacity():
    with pytest.raises(ValueError, match="invalid capacity"):
        dock_status(0, 0)


def test_dock_rejects_a_negative_bike_count():
    with pytest.raises(ValueError, match="invalid bike count"):
        dock_status(-1, 10)


@pytest.mark.parametrize(
    ("bikes", "capacity", "expected"),
    [
        (0, 10, "empty"),
        (10, 10, "full"),
        (2, 10, "few bikes"),
        (8, 10, "few slots"),
        (5, 10, "available"),
    ],
)
def test_dock_status_messages(bikes, capacity, expected):
    assert dock_status(bikes, capacity) == expected


def test_active_rider_cannot_unlock_another_bike():
    assert can_unlock(100, True, 25) is False


def test_underage_rider_cannot_unlock():
    assert can_unlock(100, False, 15) is False


def test_minor_with_enough_balance_can_unlock():
    assert can_unlock(100, False, 17) is True


def test_adult_with_enough_balance_can_unlock():
    assert can_unlock(50, False, 18) is True
