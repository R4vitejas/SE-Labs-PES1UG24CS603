"""Second pass: exercise decisions that the line-focused tests leave open."""

from bike_share_rental import ride_cost


def test_regular_ride_has_no_extra_fees():
    # Two standard blocks, no subscription, peak fee or long-ride fee.
    assert ride_cost("standard", 45, False, False) == 40


def test_subscriber_cargo_ride_still_costs_one_block():
    # The free block does not make a 60-minute ride free.
    # Cargo bikes also do not get the peak surcharge.
    assert ride_cost("cargo", 60, True, True) == 50
